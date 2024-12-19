from typing import Optional
import typer
from typing_extensions import Annotated

from jamie import filer
from jamie.downloader import download_audio
from jamie.scorer import score_quotes
from jamie.splitter import split_audio
from jamie.transcribe import process_audio

app = typer.Typer()


@app.callback()
def callback():
    """
    Awesome Portal Gun
    """


@app.command()
def download(
    url: str = typer.Argument(),
    filename: Annotated[Optional[str], typer.Option()] = None,
    extension: Annotated[str, typer.Option()] = ".mp3",
):
    """
    Download YouTube video
    """
    typer.echo("Downloading YouTube video")
    download_audio(url, filename, extension)


@app.command()
def split(
    filename: str = typer.Argument(),
    duration:str = typer.Option(),
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


@app.command()
def process(
    filename: str = typer.Argument(),
    episode: str = typer.Argument(),
    link: str = typer.Argument(),
):
    """
    Shoot the portal gun
    """
    typer.echo("Shooting portal gun")
    download_audio([link], filename)
    split_audio(filename)
    process_audio(filename)
    combine(filename)
    enhance(filename, episode, link)


def process_video(
    filename: str = typer.Argument(),
    episode: str = typer.Argument(),
    link: str = typer.Argument(),
):
    download_audio([link], filename)
    split_audio(filename)
    process_audio(filename)
    combine(filename)
    enhance(filename, episode, link)


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
    model: Annotated[str, typer.Argument()] = "quote",
    # model: str = typer.Option(default="quote"),
):
    """
    WIP: Score quotes using custom LLM
    """
    typer.echo("Scoring transcripts using LLM")
    score_quotes(filename, model)
