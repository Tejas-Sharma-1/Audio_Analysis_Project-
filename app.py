import streamlit as st
import os

st.set_page_config(
    page_title="Podcast Transcript Navigator",
    layout="wide",
    initial_sidebar_state="collapsed"
)
st.markdown("""
<style>
div[data-baseweb="input"] input {
    background-color: transparent !important;
    color: inherit !important;
}
div[data-baseweb="input"] input:hover,
div[data-baseweb="input"] input:focus {
    border-color: white !important;
    box-shadow: 0 0 0 1px white !important;
    outline: none !important;
}
div[data-baseweb="select"] > div {
    background-color: transparent !important;
    border-color: white !important;
}

div[data-baseweb="select"] > div:hover {
    border-color: white !important;
    box-shadow: none !important;
}

div[data-baseweb="select"] > div:focus-within {
    border-color: white !important;
    box-shadow: 0 0 0 1px white !important;
}

div[data-baseweb][data-error="true"] {
    border-color: white !important;
    box-shadow: none !important;
}

.transcript-box {
    padding: 1.8rem;
    border-radius: 14px;
    background-color: rgba(255, 255, 255, 0.05);
    line-height: 1.7;
    font-size: 1rem;
}
</style>
""", unsafe_allow_html=True)

SEGMENT_DIR = "results/advanced_segments"
segments = {}

for file in sorted(os.listdir(SEGMENT_DIR)):
    if file.endswith(".txt"):
        path = os.path.join(SEGMENT_DIR, file)
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()

        label = file.replace(".txt", "").replace("_", " ")
        segments[label] = text

st.title(" Podcast Transcript Navigator")
st.caption("Week 4 · Transcript Navigation & Segment Jumping")

col1, col2 = st.columns([1.5, 4.5])

with col1:
    search_query = st.text_input(
        "Search topic",
        placeholder="AI, ML, neural networks"
    )


if search_query:
    filtered_segments = {
        k: v for k, v in segments.items()
        if search_query.lower() in k.lower()
        or search_query.lower() in v.lower()
    }
else:
    filtered_segments = segments

with col2:
    if filtered_segments:
        selected_segment = st.selectbox(
            "Select transcript segment",
            list(filtered_segments.keys())
        )
    else:
        st.warning("No related podcast segments found.")
        st.stop()

st.markdown("---")
st.subheader(selected_segment)

st.markdown(
    f"<div class='transcript-box'>{filtered_segments[selected_segment]}</div>",
    unsafe_allow_html=True
)
