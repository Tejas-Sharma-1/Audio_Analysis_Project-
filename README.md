# Audio Analysis Project

## Overview
This project focuses on preparing podcast audio data for Speech-to-Text and NLP based tasks.  
The main goal is to perform proper audio preprocessing and generate accurate transcripts that can be used for further analysis such as topic segmentation and keyword extraction

## Step 1: Audio Preprocessing

Audio preprocessing was done to ensure that all audio files have a consistent and clean format before transcription.

The following steps were performed:
- Converted all audio files to **WAV format**
- Resampled audio to **16 kHz**
- Converted audio to **mono channel**
- Applied **noise reduction** and **loudness normalization** using standard audio preprocessing tools
- Trimmed unnecessary intro and outro sections
- Split long audio files into **20–30 second chunks**

These steps help improve transcription accuracy and ensure compatibility with ASR models.
## Step 2: Transcript Preparation

- Transcripts were generated using the **Whisper** pretrained ASR model
- Transcription was executed using **Google Colab** for environment compatibility
- Start and end **timestamps were preserved**
- Transcripts were saved in **JSON format**
- Alignment between audio chunks and transcripts was maintained

## Folder Structure
raw_audio/ # Original audio files
standardized_audio/ # WAV, 16kHz, mono audio
processed_chunks/ # Trimmed and chunked audio files
transcripts/ # Whisper transcript outputs (JSON)

## Scripts Used

- standardize_audio.py  
  Converts audio to WAV format, 16 kHz sample rate, and mono channel.

- audio_preprocessing.py
  Trims audio and splits long files into smaller chunks.

- clean_transcripts.py 
  Performs basic text cleaning on transcript outputs.

## Tools & Technologies

- Python
- Pydub
- Google Colab
- Whisper ASR
- Audio preprocessing tools


