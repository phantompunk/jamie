from pathlib import Path
from typing import Optional

import typer
from typing_extensions import Annotated

from jamie import filer
from jamie.downloader import download_audio
from jamie.scorer import score_quotes
from jamie.splitter import split_audio
from jamie.transcribe import process_audio

app = typer.Typer()

HELP_URL = "Required YouTube video url"
HELP_NAME = "Name for the downloaded audio file"
HELP_FORMAT = "Audio file type (mp3, m4a,)"
HELP_EPISODE = "Episode number used for quote metadata"
HELP_DURATION = "Split audio file into chunks by duration in seconds"
HELP_SPEAKER = "Name of the speaker that matches the transcription"
HELP_MODEL = "Name of the OLLAMA model to use"


def validate_format(value: str):
    """Validates that the given format is either 'mp3' or 'm4a', case-insensitive and allowing a leading dot."""
    supported_formats = {"mp3", "wav"}

    # Normalize input
    normalized_value = value.lower().lstrip(".")

    if normalized_value not in supported_formats:
        raise typer.BadParameter(
            f"Invalid format: {value}. Supported formats: {', '.join(supported_formats)}"
        )

    return normalized_value


@app.command()
def download(
    url: Annotated[str, typer.Argument(help=HELP_URL)],
    name: Annotated[Optional[str], typer.Option(help=HELP_NAME)] = None,
    format: Annotated[
        Optional[str], typer.Option(help=HELP_FORMAT, callback=validate_format)
    ] = None,
):
    """
    Download audio from YouTube video
    """
    typer.echo("Downloading YouTube video")
    filename = download_audio(url, name, format)[0]
    typer.echo(f"Downloaded YouTube video as: {filename}")


@app.command()
def split(
    filename: Annotated[str, typer.Argument(help=HELP_NAME)],
    duration: Annotated[int, typer.Option(help=HELP_DURATION)] = 300,
):
    """
    Split audio file into segments of a given duration (Default 300 seconds)
    """
    typer.echo(f"Splitting audio file: {filename}")
    files, parts = split_audio(filename, duration=duration)
    typer.echo(f"Split audio into {parts} parts: {files}")


@app.command()
def transcribe(
    filename: Annotated[str, typer.Argument(help="File or glob matching files")],
    duration: Annotated[int, typer.Option(help=HELP_DURATION)] = 300,
):
    """
    Transcribe an audio file
    """
    typer.echo("Transcribing audio file")
    process_audio(filename, duration)
    typer.echo("Completed transcribing audio file")


@app.command()
def process(
    url: Annotated[str, typer.Argument(help=HELP_URL)],
    duration: Annotated[int, typer.Option(help=HELP_DURATION)] = 300,
    name: Annotated[Optional[str], typer.Option(help=HELP_NAME)] = "",
    format: Annotated[
        Optional[str], typer.Option(help=HELP_FORMAT, callback=validate_format)
    ] = "mp3",
    episode: Annotated[Optional[str], typer.Option(help=HELP_EPISODE)] = None,
):
    """
    Download, split, transcribe, combine and enhance YouTube video
    """
    typer.echo(f"Processing video url {url}")
    filename = download_audio(url, name, format)
    file_pattern = split_audio(filename, duration=duration)
    newfile = process_audio(file_pattern, duration=duration)
    # combine(name)
    filer.enhance(newfile, url, episode)
    typer.echo("Completed processing transcripts")


@app.command()
def merge(
    filename: Annotated[str, typer.Argument(help=HELP_NAME)],
):
    """
    Combine consecutive passages by the same speaker.
    """
    typer.echo("Combining sequential spoken sections")
    filer.merge(filename)
    typer.echo("Completed combining transcripts")


@app.command()
def enhance(
    filename: Annotated[str, typer.Argument(help=HELP_NAME)],
    url: Annotated[Optional[str], typer.Option(help=HELP_URL)] = None,
    episode: Annotated[Optional[str], typer.Option(help=HELP_EPISODE)] = None,
    speaker0: Annotated[Optional[str], typer.Option(help=HELP_SPEAKER)] = None,
    speaker1: Annotated[Optional[str], typer.Option(help=HELP_SPEAKER)] = None,
    speaker2: Annotated[Optional[str], typer.Option(help=HELP_SPEAKER)] = None,
):
    """
    Enhance quotes with metadata: episode, link
    """
    typer.echo("Enhancing transcripts with meta data")
    filer.enhance(filename, url, episode, speaker0, speaker1, speaker2)
    typer.echo("Completed enhancing transcripts")


@app.command()
def score(
    filename: Annotated[str, typer.Argument(help=HELP_NAME)],
    model: Annotated[Optional[str], typer.Option(help=HELP_MODEL)] = None,
):
    """
    WIP: Score quotes using custom LLM
    """
    typer.echo("Scoring transcripts using LLM")
    score_quotes(filename, model)
    typer.echo("Completed scoring transcripts")
