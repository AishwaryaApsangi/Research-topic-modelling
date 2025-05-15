import seaborn as sns
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from gensim.models.phrases import Phrases, Phraser

st.set_page_config(page_title="Topic Phrase Explorer", layout="wide")
st.title("🧩 Topic Phrase Explorer")

# Check session state for model
required_keys = ["lda_model", "dictionary", "tokenized"]
if not all(key in st.session_state for key in required_keys):
    st.warning("⚠️ Please visit the WordCloud tab first to load the model.")
    st.stop()

# Load from session
lda_model = st.session_state.lda_model
dictionary = st.session_state.dictionary
tokenized = st.session_state.tokenized

# === Build bigrams/trigrams ===
st.sidebar.subheader("Phrase Modeling")
min_count = st.sidebar.slider("Min Phrase Count", 1, 5, 2)
threshold = st.sidebar.slider("Phrase Sensitivity Threshold", 1, 15, 10)

bigram = Phrases(tokenized, min_count=min_count, threshold=threshold)
trigram = Phrases(bigram[tokenized], threshold=threshold)
trigram_mod = Phraser(trigram)

# Apply trigram model to tokenized docs
phrased_docs = [trigram_mod[bigram[doc]] for doc in tokenized]

# === Extract topic phrases ===
num_topics = lda_model.num_topics
top_n = st.slider("Top Phrases per Topic", 5, 20, 10)
topic_phrases = {}

for i in range(num_topics):
    terms = lda_model.get_topic_terms(i, topn=30)
    phrases = [(dictionary[id], round(weight, 4)) for id, weight in terms if '_' in dictionary[id]]
    topic_phrases[f"Topic {i + 1}"] = phrases[:top_n]

# === Display topic phrase table ===
rows = []
for topic, phrases in topic_phrases.items():
    for phrase, weight in phrases:
        rows.append({"Topic": topic, "Phrase": phrase.replace("_", " "), "Weight": weight})

df = pd.DataFrame(rows)

# Show as interactive table
st.subheader("🔗 Top Multi-Word Phrases by Topic")
st.dataframe(df, use_container_width=True)

# === New Visualization: Heatmap of Phrase Weights ===
st.subheader("🔥 Phrase Importance Heatmap")
if not df.empty:
    heatmap_data = df.pivot(index="Phrase", columns="Topic", values="Weight").fillna(0)
    fig, ax = plt.subplots(figsize=(10, max(4, 0.4 * len(heatmap_data))))
    sns.heatmap(heatmap_data, annot=True, cmap="YlGnBu", fmt=".2f", cbar_kws={"label": "Weight"}, ax=ax)
    ax.set_title("Phrase Distribution Across Topics")
    st.pyplot(fig)
else:
    st.info("No phrases were detected for the selected settings.")
