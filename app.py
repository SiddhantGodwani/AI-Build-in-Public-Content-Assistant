
import streamlit as st
import requests
import os

st.set_page_config(page_title="Build-in-Public Post Generator", layout="centered")

st.title("🚀 AI Build-in-Public Post Generator (Gemini Edition)")
st.markdown("Use Google Gemini to generate authentic, engaging posts for your product-building journey.")

with st.sidebar:
    st.header("🔐 Gemini API Settings")
    api_key = st.text_input("Enter your Google API Key", type="password", help="Get one from https://makersuite.google.com/app/api")
    st.markdown("[Get API Key](https://makersuite.google.com/app/api)")

with st.form("post_form"):
    st.subheader("📋 Describe Your Update")
    progress = st.text_input("🛠️ What did you build/work on?")
    challenge = st.text_area("💬 Any challenge, insight, or story?", height=100)
    tone = st.selectbox("🎭 Tone", ["Casual", "Witty", "Inspirational"])
    platform = st.selectbox("📱 Platform", ["Twitter", "LinkedIn", "Instagram"])
    submit = st.form_submit_button("✨ Generate Post")

def generate_post_gemini(api_key, prompt):
    endpoint = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
    headers = {"Content-Type": "application/json"}
    body = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }
    params = {"key": api_key}
    try:
        response = requests.post(endpoint, headers=headers, params=params, json=body)
        result = response.json()
        return result["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        return f"❌ Error: {str(e)}"

if submit:
    if not api_key:
        st.warning("⚠️ Please enter your Gemini API key in the sidebar.")
    elif not progress:
        st.warning("⚠️ Please describe what you worked on.")
    else:
        with st.spinner("Talking to Gemini..."):
            final_prompt = f"""
You're an assistant that helps product builders create build-in-public social media posts.

User progress: {progress}
Challenge or story: {challenge if challenge else "None"}
Platform: {platform}
Tone: {tone}

Please generate a complete post with:
1. A hook to grab attention
2. A short explanation of what was built
3. (Optional) An insight or obstacle
4. A question or CTA at the end

Keep it under 280 characters for Twitter, paragraphs for LinkedIn, and friendly with line breaks for Instagram.

Avoid generic phrases like 'crushing it', 'grind', or excessive emojis.

Final Output:
"""
            output = generate_post_gemini(api_key, final_prompt)
            st.success("✅ Here's your generated post:")
            st.text_area("Generated Post", value=output.strip(), height=200)
