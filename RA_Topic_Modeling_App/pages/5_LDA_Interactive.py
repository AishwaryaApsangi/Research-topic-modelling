import streamlit as st
import plotly.express as px

st.title("🧠 Interactive LDA Topic Explorer")

lda_model = st.session_state.get("lda_model")

if not lda_model:
    st.error("Please run the 'LDA Word Clouds' tab first to initialize the model.")
else:
    num_topics = lda_model.num_topics
    selected_topic = st.slider("Select Topic Number", min_value=1, max_value=num_topics, value=1)
    num_words = st.slider("Number of Top Words", min_value=5, max_value=30, value=10)

    topic_words = lda_model.show_topic(selected_topic - 1, topn=num_words)
    words = [word for word, prob in topic_words]
    probs = [prob for word, prob in topic_words]

    st.markdown(f"### Topic {selected_topic} — Top {num_words} Words")

    fig = px.bar(
        x=probs,
        y=words,
        orientation='h',
        labels={'x': 'Probability', 'y': 'Word'},
        color=probs,
        color_continuous_scale="plasma",
        title=f"Top {num_words} words for Topic {selected_topic}"
    )
    fig.update_layout(yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig, use_container_width=True)
