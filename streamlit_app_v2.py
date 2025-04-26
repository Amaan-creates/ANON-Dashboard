# ANON V3.2 - Executive Dashboard for Tata AutoComp

import streamlit as st
import pandas as pd
import plotly.express as px
from bertopic import BERTopic
from datetime import datetime
from PIL import Image
from wordcloud import WordCloud

# --- PAGE CONFIG ---
st.set_page_config(page_title="ANON V3.2 | Tata AutoComp", layout="wide", page_icon="📊")

# --- HEADER ---
st.markdown("""
    <div style="background-color:#0066b3;padding:1rem;border-radius:8px;margin-bottom:1rem;text-align:center;">
        <h1 style="color:white;">ANON: Tata AutoComp Innovation Hub</h1>
    </div>
""", unsafe_allow_html=True)

# --- LOGO ---
try:
    logo = Image.open('tata_autocomp_systems_ltd_logo.jpeg')
    st.sidebar.image(logo, width=150)
except:
    st.sidebar.warning("Logo not found.")

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("Navigation")
page = st.sidebar.radio("", ["🏠 Dashboard", "🧩 Submit Idea", "🧠 AI Insights", "🔄 Tone Translator", "📥 Export"])

# --- INITIALIZE DATA ---
if 'ideas_df' not in st.session_state:
    sample_ideas = [
        "Cross-team collaboration is slow.",
        "Promotion pathways are unclear.",
        "Improve EV battery assembly documentation.",
        "Too many meetings delay project sprints.",
        "Deadline pressure impacts mental health."
    ]
    moods = ["😠", "🙂", "🤔", "😐", "😊"]
    st.session_state.ideas_df = pd.DataFrame([{
        'text': idea,
        'mood': moods[i % 5],
        'timestamp': datetime.now(),
        'status': "🟡 New"
    } for i, idea in enumerate(sample_ideas)])

ideas_df = st.session_state.ideas_df

# --- DASHBOARD PAGE ---
if page == "🏠 Dashboard":
    with st.container():
        st.subheader("👋 Welcome back, Anonymous Innovator!")
        st.markdown("*Leadership with Trust — Tata AutoComp.*")
        st.divider()

    # KPI Cards
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("💡 Total Ideas", len(ideas_df))
    with col2:
        most_common_mood = ideas_df['mood'].mode()[0] if not ideas_df.empty else "N/A"
        st.metric("😊 Top Mood", most_common_mood)
    with col3:
        positivity = (ideas_df['mood'].value_counts().get("😊", 0) / len(ideas_df)) * 100 if len(ideas_df) > 0 else 0
        st.metric("🚀 Positivity Rate", f"{positivity:.1f}%")

    st.divider()

    # Mood Trend Chart
    st.markdown("### 📈 Mood Trend Over Time")
    mood_counts = ideas_df.groupby(ideas_df['timestamp'].dt.date).size()
    fig_trend = px.line(x=mood_counts.index, y=mood_counts.values, labels={'x': 'Date', 'y': 'Ideas Submitted'}, markers=True)
    fig_trend.update_layout(
        plot_bgcolor='#0E1117',
        paper_bgcolor='#0E1117',
        font_color='white',
        xaxis_title_font=dict(color='white'),
        yaxis_title_font=dict(color='white')
    )
    fig_trend.update_traces(line=dict(color="#66b2ff", width=3))
    st.plotly_chart(fig_trend, use_container_width=True)

    st.divider()

    # Mood Donut Chart
    st.markdown("### 📊 Mood Distribution")
    mood_dist = ideas_df['mood'].value_counts()
    fig_donut = px.pie(values=mood_dist.values, names=mood_dist.index, hole=0.5,
                       color_discrete_sequence=["#79B4B7", "#A9D6E5", "#F4F1BB", "#FFD6A5", "#FFADAD"])
    fig_donut.update_traces(textinfo='percent+label', pull=[0.05]*len(mood_dist))
    fig_donut.update_layout(
        showlegend=True,
        plot_bgcolor='#0E1117',
        paper_bgcolor='#0E1117',
        font_color='white'
    )
    st.plotly_chart(fig_donut, use_container_width=True)

# --- SUBMIT IDEA PAGE ---
elif page == "🧩 Submit Idea":
    st.subheader("🧩 Submit a New Idea")
    with st.form("submit_form"):
        idea_text = st.text_area("Share your anonymous idea:")
        mood_choice = st.radio("How do you feel?", ["😠 Frustrated", "🙂 Hopeful", "🤔 Confused", "😐 Neutral", "😊 Excited"])
        submit = st.form_submit_button("Submit")
        if submit:
            if idea_text.strip():
                new_row = {
                    "text": idea_text.strip(),
                    "mood": mood_choice,
                    "timestamp": datetime.now(),
                    "status": "🟡 New"
                }
                st.session_state.ideas_df = pd.concat([st.session_state.ideas_df, pd.DataFrame([new_row])], ignore_index=True)
                st.success("✅ Idea submitted successfully!")
                st.experimental_rerun()
            else:
                st.warning("Please write an idea before submitting.")

# --- AI INSIGHTS PAGE ---
elif page == "🧠 AI Insights":
    st.subheader("🧠 Topic Clustering Insights")
    if len(ideas_df) > 2:
        topic_model = BERTopic(language="english", umap_model=None, verbose=False)
        topics, _ = topic_model.fit_transform(ideas_df["text"])
        ideas_df['topic'] = topics

        fig_topics = topic_model.visualize_barchart(top_n_topics=5)
        st.plotly_chart(fig_topics, use_container_width=True)

        st.markdown("### Top Topics Detected:")
        st.dataframe(topic_model.get_topic_info().head(5))
    else:
        st.warning("Not enough ideas yet for clustering. Need at least 3.")

# --- TONE TRANSLATOR PAGE ---
elif page == "🔄 Tone Translator":
    st.subheader("🔄 Language/Tone Translator")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Enter Engineering/Technical Language:**")
        tech_input = st.text_area("Engineering phrasing", placeholder="e.g., 'Server response latency exceeded threshold.'")
        tone_option = st.selectbox("Select Tone Style", ["Formal", "Action-Oriented", "Soft Reassurance"])

    with col2:
        st.markdown("**Management-Friendly Version:**")
        if tech_input.strip():
            if tone_option == "Formal":
                output = f"Observations indicate that '{tech_input}' is impacting performance. A review is underway to address this promptly."
            elif tone_option == "Action-Oriented":
                output = f"We are actively mitigating the issue: '{tech_input}'. Teams are implementing corrective actions."
            elif tone_option == "Soft Reassurance":
                output = f"While '{tech_input}' has been detected, proactive measures are underway to ensure system stability."
            else:
                output = "Translation in progress..."
            st.success(output)
        else:
            st.info("Waiting for input...")

# --- EXPORT PAGE ---
elif page == "📥 Export":
    st.subheader("📥 Export Data")
    st.dataframe(ideas_df)
    csv = ideas_df.to_csv(index=False).encode('utf-8')
    st.download_button("Download CSV", csv, "anon_dashboard_data.csv", "text/csv")
