import streamlit as st
import os
import re
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from wordcloud import WordCloud
import matplotlib.pyplot as plt
nltk.download('vader_lexicon')

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Podcast Transcript Navigator",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------- STYLES ----------------
st.markdown("""
<style>
.block-container { padding-top: 2rem; }

.segment-item {
    padding: 0.65rem 0.75rem;
    margin-bottom: 0.35rem;
    background-color: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 6px;
}

.segment-active {
    background-color: rgba(99,102,241,0.18);
    border-left: 4px solid #6366f1;
}

.section-title {
    font-size: 0.75rem;
    letter-spacing: 0.14em;
    opacity: 0.55;
    margin-bottom: 0.6rem;
}

.transcript-box {
    background-color: rgba(255,255,255,0.04);
    border-radius: 10px;
    padding: 1.6rem;
    line-height: 1.75;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HELPERS ----------------
def extract_chunk_index(filename):
    return int(filename.split("_chunk_")[1].split(".")[0])

def polish_summary(text):
    if not text:
        return ""
    fillers = ["um", "you know", "like"]
    for f in fillers:
        text = re.sub(rf"\b{f}\b", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s+", " ", text).strip()
    sentences = re.split(r'(?<=[.!?]) +', text)[:3]
    return " ".join(s.capitalize() for s in sentences)

# ---------------- SENTIMENT ----------------
sentiment_analyzer = SentimentIntensityAnalyzer()

def analyze_sentiment(text):
    score = sentiment_analyzer.polarity_scores(text)["compound"]
    if score >= 0.05:
        return "Positive", score
    elif score <= -0.05:
        return "Negative", score
    return "Neutral", score

# ---------------- PATHS ----------------
SEGMENT_DIR = "results/advanced_segments"
SUMMARY_DIR = "results/summaries"
KEYWORD_DIR = "results/embedding_results/keywords"

CUSTOM_STOPWORDS = {
    "data","today","looking","feel","feeling",
    "episode","podcast","host","welcome",
    "content","talking","people"
}

def load_summary(idx):
    path = os.path.join(SUMMARY_DIR, f"Podcast1_chunk_{idx}_summary.txt")
    if not os.path.exists(path):
        return ""
    with open(path, "r", encoding="utf-8") as f:
        return polish_summary(f.read().strip())

def load_keywords(idx):
    path = os.path.join(KEYWORD_DIR, f"Podcast1_chunk_{idx}_keywords.txt")
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return [
            line.strip().lower()
            for line in f.readlines()
            if line.strip() and "keywords" not in line.lower()
        ]

# ---------------- LOAD SEGMENTS (DEDUPLICATED) ----------------
segments = {}
for file in sorted(os.listdir(SEGMENT_DIR), key=extract_chunk_index):
    if not file.endswith(".txt"):
        continue

    idx = extract_chunk_index(file)

    # ✅ Ignore duplicate chunk files
    if idx in segments:
        continue

    with open(os.path.join(SEGMENT_DIR, file), "r", encoding="utf-8") as f:
        transcript = f.read().strip()

    sentiment_label, sentiment_score = analyze_sentiment(transcript)

    segments[idx] = {
        "id": idx,
        "label": f"Segment {idx + 1}",
        "transcript": transcript,
        "summary": load_summary(idx),
        "sentiment_label": sentiment_label,
        "sentiment_score": sentiment_score,
        "keywords": load_keywords(idx)
    }

segments = list(segments.values())

# ---------------- HEADER ----------------
st.title("🎙️ Podcast Transcript Navigator")
st.caption("Milestone· Visualization and Detail Enhancements")

# ---------------- STATE ----------------
if "selected_id" not in st.session_state:
    st.session_state.selected_id = segments[0]["id"]

# ---------------- LAYOUT ----------------
left, right = st.columns([0.8, 3.12])

# ---------------- LEFT PANEL (DESKTOP MAIN) ----------------
# ---------------- LEFT PANEL ----------------
with left:
    st.markdown("### 🎯 Segments")

    # Scrollable container (native Streamlit)
    with st.container(height=450):
        for seg in segments:
            active = seg["id"] == st.session_state.selected_id

            if st.button(
                f"{'👉 ' if active else ''}{seg['label']}",
                key=f"seg_{seg['id']}",
                use_container_width=True
            ):
                st.session_state.selected_id = seg["id"]
 #______________________Right Panel ___________________
selected_seg = next(s for s in segments if s["id"] == st.session_state.selected_id)

# ---------------- AUDIO SETUP (CHUNK-BASED) ----------------
CHUNK_AUDIO_DIR = "processed_chunks"

def get_chunk_audio(segment):
    chunk_id = segment["id"]

    # Try matching chunk audio (WAV format)
    possible_files = [
        f"Podcast1_chunk_{chunk_id}.wav"
    ]

    for file in possible_files:
        path = os.path.join(CHUNK_AUDIO_DIR, file)
        if os.path.exists(path):
            return path

    return None

with right:
    # ---------------- TITLE ----------------
    st.markdown("<div class='section-title'>TITLE</div>", unsafe_allow_html=True)
    st.subheader(selected_seg["label"])

    # ---------------- AUDIO (SYNCED WITH SEGMENT) ----------------
    st.markdown("<div class='section-title'>AUDIO</div>", unsafe_allow_html=True)

    audio_path = get_chunk_audio(selected_seg)

    if audio_path:
        st.audio(audio_path)
    else:
        st.warning("Chunk audio not found for this segment.")

    # ---------------- SUMMARY ----------------
    st.markdown("<div class='section-title'>SUMMARY</div>", unsafe_allow_html=True)
    
    summary = selected_seg["summary"]
    if not summary:
        summary = polish_summary(selected_seg["transcript"][:300])

    st.write(summary)

    # ---------------- SENTIMENT ----------------
    st.markdown("<div class='section-title'>SENTIMENT</div>", unsafe_allow_html=True)
    icon = {"Positive": "🟢", "Neutral": "🟡", "Negative": "🔴"}
    st.markdown(
        f"**{icon[selected_seg['sentiment_label']]} {selected_seg['sentiment_label']}** "
        f"(score: `{selected_seg['sentiment_score']:.2f}`)"
    )

    # ---------------- KEYWORDS ----------------
    st.markdown("<div class='section-title'>KEYWORDS</div>", unsafe_allow_html=True)
    if selected_seg["keywords"]:
        wc = WordCloud(
            width=600,
            height=200,
            background_color="white",
            colormap="Blues",
            stopwords=CUSTOM_STOPWORDS,
            max_words=25,
            collocations=False
        ).generate(" ".join(selected_seg["keywords"]))

        fig, ax = plt.subplots(figsize=(4, 1.6))
        ax.imshow(wc, interpolation="bilinear")
        ax.axis("off")
        st.pyplot(fig)
    else:
        st.info("No keywords available.")

    # ---------------- SEARCH ----------------
    st.markdown("<div class='section-title'>SEARCH</div>", unsafe_allow_html=True)
    query = st.text_input("🔍 Search in transcript")

    filtered_text = selected_seg["transcript"]
    if query:
        filtered_text = " ".join(
            [line for line in selected_seg["transcript"].split('.') if query.lower() in line.lower()]
        )

    # ---------------- TRANSCRIPT ----------------
    st.markdown("<div class='section-title'>TRANSCRIPT</div>", unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class='transcript-box' style="max-height:300px; overflow-y:auto;">
        {filtered_text}
        </div>
        """,
        unsafe_allow_html=True
    )