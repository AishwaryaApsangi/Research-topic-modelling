import streamlit as st
import os
import re
import nltk
import pandas as pd
from nltk.sentiment import SentimentIntensityAnalyzer

# Download resources once
nltk.download("punkt")
nltk.download("vader_lexicon")

# Load analyzer
sia = SentimentIntensityAnalyzer()

# File path
folder_path = "transcripts_cleaned"

# Streamlit UI
st.title("🧠 Quote-Level Sentiment Explorer")
st.markdown("Explore participant sentiment from each cleaned transcript.")

# Load and analyze transcripts
sentiment_rows = []

for filename in os.listdir(folder_path):
    if filename.endswith(".txt"):
        with open(os.path.join(folder_path, filename), "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                line = line.strip()
                if line and not re.match(r"(amanda|interviewer|sargent|corwin|emily|bodhi|ben|aarav|annelise|alfred):", line.lower()):
                    scores = sia.polarity_scores(line)
                    sentiment_rows.append({
                        "Transcript": filename,
                        "Quote": line,
                        "Positive": scores["pos"],
                        "Neutral": scores["neu"],
                        "Negative": scores["neg"],
                        "Compound": scores["compound"]
                    })

# Convert to DataFrame
df = pd.DataFrame(sentiment_rows)

# Display filterable table
st.dataframe(df, use_container_width=True)

# Plot average compound score per transcript
st.subheader("📈 Average Sentiment per Transcript")
avg_sentiment = df.groupby("Transcript")["Compound"].mean().reset_index()
st.bar_chart(avg_sentiment.set_index("Transcript"))
