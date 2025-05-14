import streamlit as st
import random
from collections import defaultdict
from gensim import corpora, models

st.title("Quote-Level Examples by Topic with TF-IDF Weighting")

# Load from session state
tokenized = st.session_state.get("tokenized")
docs = st.session_state.get("docs")
dictionary = st.session_state.get("dictionary")

if not all([tokenized, docs, dictionary]):
    st.error("Please visit the 'LDA Word Clouds' tab first to load models.")
    st.stop()

# TF-IDF weighting
st.subheader("🔍 Topic Modeling Using TF-IDF")
num_topics = st.slider("Number of Topics", 2, 10, 4)

bow_corpus = [dictionary.doc2bow(doc) for doc in tokenized]
tfidf_model = models.TfidfModel(bow_corpus)
tfidf_corpus = tfidf_model[bow_corpus]

# Train LDA on TF-IDF-weighted corpus
lda_tfidf_model = models.LdaModel(
    corpus=tfidf_corpus,
    id2word=dictionary,
    num_topics=num_topics,
    random_state=0,
    passes=10,
    eval_every=None
)
st.session_state["lda_tfidf_model"] = lda_tfidf_model

# Show topic-word distributions
st.markdown("### 🔡 TF-IDF Topics Overview")
for i in range(num_topics):
    top_words = ", ".join([w for w, _ in lda_tfidf_model.show_topic(i, topn=6)])
    st.markdown(f"**Topic {i+1}**: {top_words}")

# Display top quotes per topic
st.markdown("### 💬 Representative Quotes per Topic")
top_docs = defaultdict(list)
for i, doc in enumerate(tfidf_corpus):
    topics = lda_tfidf_model.get_document_topics(doc)
    top_topic = max(topics, key=lambda x: x[1])[0]
    top_docs[top_topic].append(docs[i])

for topic, quotes in top_docs.items():
    st.markdown(f"**Topic {topic+1}**")
    top_words = ", ".join([w for w, _ in lda_tfidf_model.show_topic(topic, topn=6)])
    st.caption(f"Top words: {top_words}")
    for q in random.sample(quotes, min(2, len(quotes))):
        st.info(q[:350] + "...")
