# -*- coding: utf-8 -*-
import os
import json

SEGMENTS_DIR = "results/baseline_segments"

segments = []
segment_files = sorted(os.listdir(SEGMENTS_DIR))

segment_id = 1
start_time = 0

for file in segment_files:
    file_path = os.path.join(SEGMENTS_DIR, file)

    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read().strip()

    # Fake timing (acceptable for Week 5 if timestamps are optional)
    duration = 30
    end_time = start_time + duration

    segments.append({
        "id": segment_id,
        "start_time": start_time,
        "end_time": end_time,
        "title": f"Segment {segment_id}",
        "summary": text[:200] + "..." if len(text) > 200 else text,
        "keywords": [],
        "sentiment": {
            "label": "Neutral",
            "score": 0.0
        }
    })

    start_time = end_time
    segment_id += 1

with open("segments.json", "w", encoding="utf-8") as f:
    json.dump(segments, f, indent=2)

print(f"Exported {len(segments)} segments to segments.json")

