import json
import logging
import os
import glob

logger = logging.getLogger()


def process_audio(pattern: str):
    import whisperx

    files = glob.glob(os.path.join("./splits", pattern), recursive=True)
    if not files:
        logger.info("No files matched the given pattern.")

    for file in files:
        print('found', file)
        # filename = os.path.basename(file).replace(".mp3", ".json")
        # audio = whisperx.load_audio(file)
        # results = transcribe_audio(audio)
        # results = diarize_audio(audio, results)
        # results = combine(results)
        #
        # logger.info(f"Writing segments to file: {pattern}")
        # data = json.dumps(results)
        # with open(f"transcripts/{filename}", "w") as file:
        #     file.write(data)


def transcribe_audio(audio):
    # logging.info(f"Transcribing: {filename}")
    import whisperx

    device = "cpu"
    batch_size = 5  # reduce if low on GPU mem
    compute_type = "int8"  # change to "int8" if low on GPU mem (may reduce accuracy)

    model_dir = "./model/"
    model = whisperx.load_model(
        "large-v2",
        device,
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

    # logging.info(f"Writing segments to file: {filename}")
    # data = json.dumps(result["segments"])
    # with open(f"segments/{filename}", "a") as file:
    #     file.write(data)

    return result


def diarize_audio(audio, result):
    # logger.info(f"Diarizing: {filename}")
    import whisperx

    device = "cpu"
    diarize_model = whisperx.DiarizationPipeline(
        use_auth_token=os.environ["HUGGINGFACE_TOKEN"], device=device
    )
    diarize_segments = diarize_model(audio, min_speakers=2, max_speakers=2)
    result = whisperx.assign_word_speakers(diarize_segments, result)

    # logger.info(f"Writing diarized segments to file: {filename}")
    # data = json.dumps(result["segments"])
    # with open(f"diarized/{filename}", "w") as file:
    #     file.write(data)

    return result["segments"]


def combine(segments):
    # logger.info("Combining: {filename}")
    words = [w for s in segments for w in s.get("words", [])]

    prev = ""
    passages, buffer = [], []
    for word in words:
        quote = word.get("word")
        speaker = word.get("speaker", "")
        if len(prev) == 0:
            prev = speaker
            buffer.append(quote)
        elif prev != speaker:
            passages.append(dict(quote=" ".join(buffer), speaker=prev))
            buffer.clear()
            buffer.append(quote)
            prev = speaker
        else:
            buffer.append(quote)

    if buffer:
        passages.append(dict(quote=" ".join(buffer), speaker=prev))

    # logger.info(f"Writing combined segments to file: {filename}")
    # data = json.dumps(passages)
    # with open(f"transcripts/{filename}", "w") as file:
    #     file.write(data)
