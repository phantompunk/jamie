import glob
import json
import os
import re
from pathlib import Path


from jamie.logger import logger
from jamie.model import Quote


def remove_yt_id(text):
    pattern = r"\[[a-zA-Z0-9]{11}\]"
    return re.sub(pattern, "", text)


def process_audio(pattern: str, duration:str="300"):
    path = Path(remove_yt_id(pattern))
    if "*" not in pattern and path.suffix in [".mp3"]:
        pattern = f"{path.stem}*"
    if "*" not in pattern:
        pattern += "*"

    # determine if pattern is a glob or split
    files = glob.glob(pattern, recursive=True)
    if not files:
        logger.info("No files matched the given pattern.")
    if not files and path.is_file():
        logger.info("Only the main file matched the given pattern.")
        files = [path.as_posix()]

    for segment, file in enumerate(files):
        logger.info(f"Processing audio file: {file}")
        filename = f"{Path(file).stem}.json"
        audio = load_audio(file)
        results = transcribe_audio(audio)
        results = diarize_audio(audio, results)
        start_at = segment * int(duration)
        segments = combine(results, start_at)

        logger.info(f"Writing segments to file: {filename}")
        data = json.dumps([s.to_dict() for s in segments])
        with open(f"./{filename}", "w") as file:
            file.write(data)


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
    # device = "cpu"
    # batch_size = 5  # reduce if low on GPU mem
    # compute_type = "int8"  # change to "int8" if low on GPU mem (may reduce accuracy)

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
    # logger.info(f"Diarizing: {filename}"

    diarize_model = whisperx.DiarizationPipeline(
        use_auth_token=os.environ["HUGGINGFACE_TOKEN"], device=device
    )
    diarize_segments = diarize_model(
        audio, min_speakers=min_speakers, max_speakers=max_speakers
    )
    result = whisperx.assign_word_speakers(diarize_segments, result)

    # print(result)
    # with open("test-segment.json", "w+") as file:
    #     json.dump(result, file)

    return result["segments"]


def combine(segments: list, start_at:int=0) -> list[Quote]:
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
            passages.append(Quote(quote=" ".join(buffer), speaker=prev, start=start+start_at))
            buffer.clear()
            buffer.append(quote)
            prev = speaker
            start = int(word.get("start","0"))
        else:
            buffer.append(quote)

    if buffer:
        passages.append(Quote(quote=" ".join(buffer), speaker=prev, start=start+start_at))
    return passages
