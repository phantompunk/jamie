import glob
import os
import re
from pathlib import Path
from tqdm import tqdm


from jamie.filer import write_json_quotes
from jamie.logger import logger
from jamie.model import Quote


def remove_yt_id(text):
    pattern = r"\[[a-zA-Z0-9]{11}\]"
    return re.sub(pattern, "", text)


def extract_number(filename):
    match = re.search(r"-(\d{3})\.", filename)
    if match:
        return int(match.group(1))
    return 0


def is_glob(pattern) -> bool:
    if any(char in pattern for char in ["*", "[", "]", "?"]):
        matched = glob.glob(pattern, recursive=True)
        return True if matched else False
    return False


def is_file(filepath) -> bool:
    if os.path.isfile(filepath):
        return True
    return False


def is_list(files) -> bool:
    if type(files) is list:
        return True
    return False


def process_audio(
    pattern: str,
    device: str,
    model_dir: str,
    max_speakers: int,
    duration: int = 300,
):
    datafile = pattern.split("-*")[0] + ".json"
    files = glob.glob(pattern, recursive=True)
    files.sort()

    if not os.getenv("HUGGINGFACE_TOKEN"):
        raise EnvironmentError(
            "Required environment variable 'HUGGINGFACE_TOKEN' is not set."
        )

    data = []
    for file in tqdm(files, desc="Transcribing audio files"):
        logger.info(f"Processing audio file: {file}")
        path = Path(file)
        audio = load_audio(path.as_posix())
        results = transcribe_audio(audio, device, model_dir=model_dir)
        results = diarize_audio(
            audio, results, device=device, max_speakers=max_speakers
        )
        start_at = extract_number(path.stem) * int(duration)
        segments = combine(results, start_at)
        data.extend(segments)

    write_json_quotes(datafile, data)
    return datafile


def load_audio(file):
    import whisperx

    return whisperx.load_audio(file)


def transcribe_audio(
    audio,
    device: str = "cpu",
    compute_type: str = "int8",
    batch_size: int = 5,
    model_dir: str = "./model/",
):
    """
    Transcribes audio using the WhisperX model.
    """
    import whisperx

    model = whisperx.load_model(
        "large-v2",
        device=device,
        compute_type=compute_type,
        download_root=model_dir,
        language="en",
    )
    result = model.transcribe(audio, batch_size=batch_size, language="en")

    model_a, metadata = whisperx.load_align_model(
        language_code=result["language"], device=device
    )
    result = whisperx.align(
        result["segments"],
        model_a,
        metadata,
        audio,
        device,
        return_char_alignments=False,
    )

    return result


def diarize_audio(
    audio, result, device: str = "cpu", min_speakers: int = 1, max_speakers: int = 2
):
    """
    Diarizes a given audio file and updates the provided transcript with speaker information.
    """
    import whisperx

    diarize_model = whisperx.DiarizationPipeline(
        use_auth_token=os.environ["HUGGINGFACE_TOKEN"], device=device
    )
    diarize_segments = diarize_model(
        audio, min_speakers=min_speakers, max_speakers=max_speakers
    )
    result = whisperx.assign_word_speakers(diarize_segments, result)

    return result["segments"]


def extract_words(segments: list):
    return [w for s in segments for w in s.get("words", [])]


def combine(segments: list, start_at: int = 0) -> list[Quote]:
    """
    Combines diarized speech segments into speaker-specific passages.
    """
    words = [w for s in segments for w in s.get("words", [])]

    prev = ""
    start = 0
    passages, buffer = [], []
    for word in words:
        quote = word.get("word")
        speaker = word.get("speaker", "")
        if len(prev) == 0:
            start = int(word.get("start", "0"))
            prev = speaker
            buffer.append(quote)
        elif prev != speaker:
            passages.append(
                Quote(quote=" ".join(buffer), speaker=prev, start=start + start_at)
            )
            buffer.clear()
            buffer.append(quote)
            prev = speaker
            start = int(word.get("start", "0"))
        else:
            buffer.append(quote)

    if buffer:
        passages.append(
            Quote(quote=" ".join(buffer), speaker=prev, start=start + start_at)
        )
    return passages
