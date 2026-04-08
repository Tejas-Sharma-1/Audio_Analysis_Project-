import os

def load_segments(folder_path):
    segments = []
    
    for idx, file in enumerate(sorted(os.listdir(folder_path))):
        if not file.endswith(".txt"):
            continue

        with open(os.path.join(folder_path, file), "r", encoding="utf-8") as f:
            text = f.read().strip()

        segments.append({
            "segment_index": idx + 1,
            "title": f"Segment {idx + 1}",
            "start_time": None,
            "end_time": None,
            "summary": "",        # we’ll plug later
            "keywords": [],       # we’ll plug later
            "sentiment": None,
            "sentiment_score": None,
            "transcript": text
        })

    return segments
