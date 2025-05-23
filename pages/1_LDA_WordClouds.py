import streamlit as st
import os
import re
import nltk
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from gensim import corpora
from gensim.models import LdaModel
import pyLDAvis.gensim_models
import streamlit.components.v1 as components

# Page title
st.title("📊 LDA Topic Word Clouds")

# === Setup stopwords and lemmatizer ===
@st.cache_data
def setup_stopwords():
    nltk.download("stopwords", quiet=True)
    return set(stopwords.words("english")).union({
        "like", "yeah", "okay", "just", "really", "actually", "thing", "gonna", "got", "well", "know", "think",
        "don’t", "didn’t", "you’re", "i’m", "right", "um", "uh", "sort", "kind", "little", "maybe", "also", "could",
        "amanda", "sargent", "bodhi", "annelise", "ben", "alfred", "corwin", "emily", "aarav"
    })

stop_words = setup_stopwords()
lemmatizer = WordNetLemmatizer()

# === Load transcripts ===
@st.cache_data
def load_docs():
    folder_path = "transcripts_cleaned"
    docs, filenames = [], []
    for fname in os.listdir(folder_path):
        if fname.endswith(".txt"):
            with open(os.path.join(folder_path, fname), "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()
                content = " ".join([line for line in lines if not line.lower().startswith(("amanda:", "interviewer:"))])
                docs.append(content)
                filenames.append(fname)
    return docs, filenames

# === Preprocessing ===
@st.cache_data
def preprocess(docs):
    from nltk.tokenize import TreebankWordTokenizer
    tokenizer = TreebankWordTokenizer()
    nltk.download("wordnet", quiet=True)

    token_lists = []
    skipped = 0

    for i, doc in enumerate(docs):
        try:
            text = re.sub(r"\s+", " ", doc.lower())
            tokens = tokenizer.tokenize(text)
            tokens = [lemmatizer.lemmatize(w) for w in tokens if w.isalpha() and w not in stop_words]

            if tokens:
                token_lists.append(tokens)
            else:
                skipped += 1
                st.warning(f"⚠️ Document {i+1} had no valid tokens and was skipped.")
        except Exception as e:
            skipped += 1
            st.warning(f"❌ Tokenization failed for document {i+1}: {e}")
    
    st.info(f"✅ Preprocessing complete. {len(token_lists)} docs used, {skipped} skipped.")
    return token_lists


# === Load + preprocess ===
docs, filenames = load_docs()
tokenized = preprocess(docs)

# === Guard clause if nothing usable ===
if not tokenized:
    st.error("❌ No valid documents to process. Check transcript files and try again.")
    st.stop()

# === Create dictionary and corpus ===
dictionary = corpora.Dictionary(tokenized)
corpus = [dictionary.doc2bow(text) for text in tokenized]
lda_model = LdaModel(corpus=corpus, num_topics=4, id2word=dictionary, passes=30, random_state=42)

# === Save to session state for use in other pages ===
st.session_state.docs = docs
st.session_state.tokenized = tokenized
st.session_state.lda_model = lda_model
st.session_state.corpus = corpus
st.session_state.dictionary = dictionary

# === WordCloud Display ===
st.subheader("🎨 Topic Word Clouds")
cols = st.columns(4)
for i in range(4):
    with cols[i]:
        wc = WordCloud(width=300, height=300, background_color="black", colormap="plasma")
        topic_words = dict(lda_model.show_topic(i, topn=30))
        fig, ax = plt.subplots()
        ax.imshow(wc.generate_from_frequencies(topic_words), interpolation="bilinear")
        ax.axis("off")
        st.markdown(f"**Topic {i + 1}**")
        st.pyplot(fig)

# === pyLDAvis Interactive Panel ===
st.subheader("📍 pyLDAvis Interactive Topic Map")
with st.expander("Show pyLDAvis Panel"):
    vis_data = pyLDAvis.gensim_models.prepare(lda_model, corpus, dictionary)
    html = pyLDAvis.prepared_data_to_html(vis_data)
    html = html.replace("background-color: #000;", "background-color: #fff;")
    components.html(html, height=800, scrolling=True)
