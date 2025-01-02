from typing import Optional

import typer
from typing_extensions import Annotated

from jamie import filer
from jamie.scorer import score_quotes
from jamie.splitter import split_audio
from jamie.transcribe import process_audio
from jamie.downloader import download_audio

app = typer.Typer()


@app.command()
def download(
    url: str = typer.Argument(help="YouTube video url"),
    name: Annotated[
        Optional[str], typer.Option(default=None,help="Optional name for the downloaded file")
    ],
    extension: Annotated[
        str,
        typer.Option(
        default=".mp3",
            case_sensitive=False,
            show_choices=True,
        ),
    ],
):
    """
    Download audio from YouTube
    """
    typer.echo("Downloading YouTube video")
    download_audio(url, name, extension)


@app.command()
def split(
    filename: str = typer.Argument(),
    duration: str = typer.Option(),
):
    """
    Split YouTube audio file by duration (Default 5min)
    """
    typer.echo("Splitting audio file")
    split_audio(filename, duration=duration)
    typer.echo(f"Completed splitting file '{filename}'")


@app.command()
def transcribe(
    filename: str = typer.Argument(),
):
    """
    Shoot the portal gun
    """
    typer.echo("Transcribing audio file")
    process_audio(filename)
    typer.echo("Completed transcribing audio file")


@app.command()
def process(
    link: str = typer.Argument(),
    episode: str = typer.Option(),
    name: str = typer.Option(),
    extension: str = typer.Option(default="mp3"),
    duration: str = typer.Option(default="300"),
):
    """
    Shoot the portal gun
    """
    typer.echo(f"Processing video url {link}")
    download_audio(link, name, extension)
    split_audio(name, duration=duration)
    process_audio(name, duration=duration)
    combine(name)
    enhance(name, episode, link)


@app.command()
def combine(
    filename: str = typer.Argument(),
):
    """
    Combines multiple JSON file transcripts into a single JSON transcript.
    """
    typer.echo("Combining sequential spoken sections")
    filer.combine_quotes(filename)


@app.command()
def enhance(
    filename: str = typer.Argument(),
    episode: str = typer.Argument(),
    link: str = typer.Argument(),
):
    """
    Enhance quotes with metadata: episode, link
    """
    typer.echo("Enhancing transcripts with meta data")
    filer.enhance_quotes(filename, episode, link)


@app.command()
def score(
    filename: str = typer.Argument(),
    model: Annotated[str, typer.Option()] = "quote",
    # model: str = typer.Option(default="quote"),
):
    """
    WIP: Score quotes using custom LLM
    """
    typer.echo("Scoring transcripts using LLM")
    score_quotes(filename, model)
    typer.echo("Completed scoring transcripts")
