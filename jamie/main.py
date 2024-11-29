from typing_extensions import Annotated
import typer

from jamie.downloader import download_audio
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
    video_url: str = typer.Argument(),
    filename: str = typer.Argument(),
    output: Annotated[str, typer.Argument()] = "./audio",
    extension: Annotated[str, typer.Argument()] = ".mp3",
):
    """
    Download YouTube video as MP3
    """
    typer.echo("Downloading YouTube video")
    download_audio([video_url],filename, output)


@app.command()
def split(
    filename: str = typer.Argument(),
):
    """
    Shoot the portal gun
    """
    typer.echo("Splitting audio file into 5 minute chunks")
    split_audio(filename)


@app.command()
def transcribe(
    filename: str = typer.Argument(),
):
    """
    Shoot the portal gun
    """
    typer.echo("Transcribing audio file")
    process_audio(filename)


def diarize():
    """
    Shoot the portal gun
    """
    typer.echo("Shooting portal gun")


@app.command()
def merge():
    """
    Shoot the portal gun
    """
    typer.echo("Merging transcription files")


@app.command()
def combine():
    """
    Shoot the portal gun
    """
    typer.echo("Combining sequential spoken sections")


@app.command()
def enhance():
    """
    Shoot the portal gun
    """
    typer.echo("Enhancing transcripts with meta data")


@app.command()
def score():
    """
    Shoot the portal gun
    """
    typer.echo("Scoring transcripts using LLM")
