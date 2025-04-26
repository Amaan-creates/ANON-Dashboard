# ANON V2: Tata AutoComp Innovation Dashboard (Streamlit version)

import streamlit as st
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
from datetime import datetime
from bertopic import BERTopic
from PIL import Image

# --- PAGE CONFIG ---
st.set_page_config(page_title="ANON Dashboard | Tata AutoComp", layout="wide", page_icon="📈")

# --- LOAD LOGO ---
logo = Image.open('tata_autocomp_systems_ltd_logo.jpeg')

# --- HEADER ---
st.sidebar.image(logo, width=150)
st.sidebar.title("Navigation")
page = st.sidebar.radio("", ["🏠 Dashboard", "🧩 Submit Idea", "🧠 AI Insights", "🔄 Tone Translator", "📥 Export"])

st.markdown("""
    <div style="background-color:#0066b3;padding:10px;border-radius:10px;margin-bottom:20px;">
        <h1 style="color:white;text-align:center;">ANON: Tata AutoComp Innovation Hub</h1>
    </div>
""", unsafe_allow_html=True)

# --- INITIALISE DATA ---
if 'ideas_df' not in st.session_state:
    sample_ideas = [
        "Cross-department collaboration is slow.",
        "Promotion paths unclear.",
        "Need for better EV assembly documentation.",
        "Meeting overload reduces project sprint speed.",
        "Wellbeing affected by workload pressure."
    ]
    moods = ["😠", "🙂", "🤔", "😐", "😊"]
    st.session_state.ideas_df = pd.DataFrame([{
        'text': idea,
        'mood': moods[i % 5],
        'timestamp': datetime.now(),
        'status': "🟡 New"
    } for i, idea in enumerate(sample_ideas)])

ideas_df = st.session_state.ideas_df

# --- PAGES ---

# 🏠 Dashboard
if page == "🏠 Dashboard":
    st.subheader("📊 Mood Dashboard")

    st.markdown("### Mood Distribution")
    mood_counts = ideas_df['mood'].value_counts()
    fig = px.bar(x=mood_counts.index, y=mood_counts.values, labels={'x': 'Mood', 'y': 'Count'}, color_discrete_sequence=['#0066b3'])
    st.plotly_chart(fig)

    st.markdown("### WordCloud of Ideas")
    text = " ".join(ideas_df["text"])
    if text.strip():
        wc = WordCloud(width=800, height=400, background_color="white").generate(text)
        st.image(wc.to_array())
    else:
        st.warning("No text available yet.")

# 🧩 Submit Idea
elif page == "🧩 Submit Idea":
    st.subheader("🧩 Submit a New Idea")
    with st.form("idea_form"):
        idea_text = st.text_area("Enter your idea:")
        mood = st.selectbox("How do you feel?", ["😠 Frustrated", "🙂 Hopeful", "🤔 Confused", "😐 Neutral", "😊 Excited"])
        submitted = st.form_submit_button("Submit")
        if submitted:
            if idea_text.strip():
                new_row = {
                    "text": idea_text.strip(),
                    "mood": mood,
                    "timestamp": datetime.now(),
                    "status": "🟡 New"
                }
                st.session_state.ideas_df = pd.concat([st.session_state.ideas_df, pd.DataFrame([new_row])], ignore_index=True)
                st.success("✅ Idea submitted successfully.")
                st.experimental_rerun()
            else:
                st.warning("Please enter a valid idea.")

# 🧠 AI Insights
elif page == "🧠 AI Insights":
    st.subheader("🧠 AI-Powered Clustering")

    if not ideas_df.empty:
        topic_model = BERTopic(language="english", verbose=False)
        topics, _ = topic_model.fit_transform(ideas_df["text"])
        ideas_df['topic'] = topics

        topic_info = topic_model.get_topic_info()
        st.dataframe(topic_info.head())

        st.plotly_chart(topic_model.visualize_topics())
    else:
        st.warning("No ideas to analyze yet.")

# 🔄 Tone Translator
elif page == "🔄 Tone Translator":
    st.subheader("🔄 Tone Translator")
    text_input = st.text_area("Enter the technical/engineering phrase:")
    if st.button("Translate"):
        if text_input.strip():
            mgmt_tone = f"We acknowledge the concern: '{text_input}'. This will be reviewed proactively."
            st.success(f"📢 Management Version:\n\n{mgmt_tone}")
        else:
            st.warning("Please enter text to translate.")

# 📥 Export
elif page == "📥 Export":
    st.subheader("📥 Export Ideas Data")
    st.dataframe(ideas_df)
    csv = ideas_df.to_csv(index=False).encode('utf-8')
    st.download_button("Download CSV", csv, file_name="anon_ideas_export.csv")
