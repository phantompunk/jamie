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
    video_url: str = typer.Argument(),
    filename: str = typer.Argument(),
    output: Annotated[str, typer.Argument()] = "./audio",
    extension: Annotated[str, typer.Argument()] = ".mp3",
):
    """
    Download YouTube video as MP3
    """
    typer.echo("Downloading YouTube video")
    download_audio([video_url], filename, output)


@app.command()
def split(
    filename: str = typer.Argument(),
    segment_time:str = typer.Option() 
):
    """
    Split YouTube audio file by duration (Default 5min)
    """
    typer.echo("Splitting audio file")
    split_audio(filename, duration=segment_time)


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
):
    """
    WIP: Score quotes using custom LLM
    """
    typer.echo("Scoring transcripts using LLM")
    score_quotes(filename)
