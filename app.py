import os

import streamlit as st
from groq import Groq


st.set_page_config(
    page_title="AI Content Assistant",
    page_icon="✍️",
    layout="centered",
)

st.title("✍️ AI Content Assistant")
st.write("Create social media content with AI using Groq.")

# Read the API key from Streamlit Cloud secrets or an environment variable.
api_key = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY"))

if not api_key:
    st.info("Add your GROQ_API_KEY in Streamlit Cloud → Settings → Secrets.")
    st.stop()

client = Groq(api_key=api_key)

content_type = st.selectbox(
    "Content Type",
    ["Social Media Post", "LinkedIn Post", "Instagram Caption", "Tweet/X Post", "Facebook Post"],
)

platform = st.selectbox(
    "Platform",
    ["LinkedIn", "Instagram", "X (Twitter)", "Facebook"],
)

topic = st.text_input(
    "Topic",
    placeholder="Example: Benefits of learning AI",
)

target_audience = st.text_input(
    "Target Audience",
    placeholder="Example: Students and beginners",
)

tone = st.selectbox(
    "Tone",
    ["Professional", "Friendly", "Educational", "Casual", "Inspirational", "Persuasive"],
)

if st.button("✨ Generate Content", type="primary"):
    if not topic.strip() or not target_audience.strip():
        st.warning("Please enter both a topic and target audience.")
        st.stop()

    prompt = f"""
Create a high-quality {content_type} for {platform}.

Topic: {topic}
Target audience: {target_audience}
Tone: {tone}

Return the result in exactly this format:

POST:
[complete post]

CAPTION:
[short engaging caption]

HASHTAGS:
[8-12 relevant hashtags]

Requirements:
- Make the content original and useful.
- Match the selected platform and tone.
- Keep it clear and easy to read.
- Do not add explanations outside the requested format.
"""

    with st.spinner("Generating content..."):
        try:
            response = client.chat.completions.create(
                model="model="openai/gpt-oss-20b",model="openai/gpt-oss-20b",",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful social media content writer.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7,
            )

            result = response.choices[0].message.content

            st.subheader("Generated Content")
            st.text_area("Your content", result, height=450)

        except Exception as e:
            st.error(f"Something went wrong: {e}")
