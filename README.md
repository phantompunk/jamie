# Jamie

Jamie is a companion tool for [jre.rest]() designed to simplify the process of downloading, splitting, and transcribing YouTube videos (eg JRE Podcasts). Its sole purpose is to help identify ~~*insightful*~~ ~~ridiculous~~~~<u>absurd</u>~~***fascinating*** quotes from the Joe Rogan Experience. Should apply easily to any interview style video.



**Key Features:**

- Downloads YouTube videos as audio files
- Splits audio files into manageable chunks for processing
- Transcribes audio using using [WhisperX]()
- Exports transcriptions as JSON



## Prerequisites 

1. Install [FFmpeg](https://ffmpeg.org/download.html)
2. Install [Poetry](https://python-poetry.org/docs/#system-requirements)
3. Create a [HuggingFace API token](https://huggingface.co/)



## Installation

Install with pip

```python
pip install git+https://github.com/phantompunk/jamie.git
```



## Usage

### Download YouTube Video

Download a YouTube video as an MP3 file.

### Split Audio

Split an audio file into multiple segments.

### Transcribe Audio

Transcribe audio files into transcript JSON files by speaker.

### Combine Audio Transcripts

Combine transcripts into a single transcript per video.

### Enhance Transcripts Audio

Update transcript JSON with metadata.

### Score Transcripts Audio

Score items in transcripts using LLM to identify meaning full quotes.



## Tech Stack

Built with modern powerful tools and frameworks for seamless audio processing and transcription:

- **[Typer](https://typer.tiangolo.com/)**: The CLI framework used to create an intuitive and user-friendly command-line interface.
- **[FFmpeg](https://ffmpeg.org/)**: A versatile multimedia framework used to slice audio files into smaller chunks.
- **[yt-dlp](https://github.com/yt-dlp/yt-dlp)**: A YouTube downloader tool that downloads and extracts audio files from YouTube videos.
- **[Poetry](https://python-poetry.org/)**: A dependency management and packaging tool used to package and distribute the CLI.
- [**Ollama**](https://github.com/ollama/ollama): Enables running open source LLMs locally
- **[WhisperX](https://github.com/m-bain/whisperx)**: An enhanced version of OpenAI’s Whisper used for transcription and speaker diarization.
  - **[faster-whisper](https://github.com/guillaumekln/faster-whisper)**: A faster implementation of Whisper, enabling efficient transcription.
  - **[pyannote-audio](https://github.com/pyannote/pyannote-audio)**: A library for speaker diarization and audio processing.
