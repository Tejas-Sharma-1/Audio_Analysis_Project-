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


## Topic Segmentation (Week 3)

After generating transcripts in Week 2, the focus of Week 3 was to convert the raw transcript text into a structured, topic-wise representation.

The transcript text was first split into sentence-level units, which served as the base input for topic segmentation algorithms.

### Topic Segmentation Algorithms Implemented

**1. Baseline Approach (TF-IDF + Cosine Similarity)**  
A sentence similarity–based baseline algorithm was implemented using TF-IDF vectorization and cosine similarity. Topic boundaries were identified by comparing similarity between consecutive sentences and detecting significant drops in similarity.

**2. Advanced Contextual TF-IDF Approach**  
An improved classical NLP approach was implemented by incorporating contextual information from neighboring sentences. This reduced abrupt topic breaks compared to the baseline method.

**3. Embedding-Based Approach (Sentence-BERT)**  
An embedding-based topic segmentation approach was implemented using Sentence-BERT. Sentence embeddings were generated and compared using cosine similarity to identify topic boundaries. This method captures semantic meaning rather than just word overlap.

---

## Algorithm Comparison and Evaluation

**Baseline TF-IDF Approach:**  
The baseline method is simple and efficient but relies on word-level overlap. As a result, topic boundaries may appear abrupt when vocabulary changes even if the topic remains the same.

**Advanced Contextual TF-IDF Approach:**  
This approach produces smoother segments than the baseline by considering sentence context. However, it still depends on surface-level word similarity.

**Embedding-Based Approach:**  
The embedding-based method captures semantic similarity between sentences, producing more meaningful segments. Topic boundaries feel more natural to a human reader, especially for conversational transcripts.

**Final Selection:**  
Based on qualitative evaluation, the embedding-based segmentation approach performed best and was selected for further processing.

---

## Step 4: Keyword Extraction and Summarization

After finalizing the topic segments, keywords were extracted for each segment using TF-IDF by removing stopwords and focusing on meaningful terms.

Short summaries (1–2 sentences) were generated for each topic segment to provide a concise description of the content.

---

## Week 3 Outputs

- Topic-wise segmented transcripts
- Keywords for each topic segment
- Short summaries for each segment

All results are stored in the `results/` directory.
