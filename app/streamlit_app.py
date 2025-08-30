from dotenv import load_dotenv
import os
import time
import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
MODEL_ID = os.environ.get("MODEL_ID")


def get_llm():
    return ChatGroq(
        model=MODEL_ID,
        temperature=0.7,
        max_tokens=None,
        timeout=None,
        max_retries=2,
        api_key=GROQ_API_KEY
    )


def build_prompt_template():
    return ChatPromptTemplate.from_messages([
        ("system", "You are a digital marketing expert, focusing on SEO and persuasive writing."),
        ("human", "{prompt}")
    ])


def format_user_prompt(subject, platform, tone, length, audience, cta, hashtags, keywords):
    text = (
        f"Topic: {subject}\n"
        f"Platform: {platform}\n"
        f"Tone: {tone}\n"
        f"Size: {length}\n"
        f"Target Audience: {audience}\n"
        f"Include CTA: {'Yes' if cta else 'No'}\n"
        f"Return Hashtags: {'Yes' if hashtags else 'No'}\n"
        f"Keywords (SEO): {keywords}"
    )
    return text


def generate_llm_stream(prompt_user):
    llm = get_llm()
    prompt_template = build_prompt_template()
    chain = prompt_template | llm
    for chunk in chain.stream({"prompt": prompt_user}):
        yield chunk.content


def main():
    st.title("Content Generator for Marketing")
    with st.form("content_form"):
        subject = st.text_input("Topic")
        platform = st.selectbox("Platform", [
            "Instagram", "Google", "YouTube", "LinkedIn", "Facebook", "E-mail", "Blog"
        ])
        tone = st.selectbox("Tone", ["Normal", "Informative", "Inspirational", "Urgent", "Informal"])
        length = st.selectbox("Length", ["Curto", "Médio", "Longo"])
        audience = st.selectbox("Target Audience", ["General", "Young Adults", "Families", "Seniors", "Teenagers"])
        cta = st.checkbox("Include CTA", False)
        hashtags = st.checkbox("Return Hashtags", False)
        keywords = st.text_area(label="Keywords (SEO)", placeholder="Preventive Medicine, Wellness, etc...")
        submitted = st.form_submit_button("Generate Content")

    if submitted:
        user_prompt = format_user_prompt(subject, platform, tone, length, audience, cta, hashtags, keywords)
        with st.spinner("Generating content..."):
            output_placeholder = st.empty()
            streamed_text = ""
            for token in generate_llm_stream(user_prompt):
                streamed_text += token
                output_placeholder.markdown(f"**Result:**\n\n{streamed_text}")
                time.sleep(0.02)


if __name__ == "__main__":
    main()