import streamlit as st
from transformers import pipeline
import requests

# Load the summarization model
@st.cache_resource  # Cache the model for faster loading
def load_summarizer():
    return pipeline("summarization", model="facebook/bart-large-cnn")

summarizer = load_summarizer()

# Define the app interface
st.title("One-Click Summary Tool")
st.write("Paste any article or text to get a quick summary!")

# Input options
input_text = st.text_area("Enter text or URL here")

# Fetch and summarize the text
if st.button("Summarize"):
    if input_text.startswith("http"):
        # If a URL is provided, fetch the text from the URL
        try:
            response = requests.get(input_text)
            input_text = response.text
        except Exception as e:
            st.error(f"Could not retrieve text from URL. Error: {e}")
    # Generate summary
    if input_text:
        summary = summarizer(input_text, max_length=150, min_length=50, do_sample=False)[0]['summary_text']
        st.subheader("Summary:")
        st.write(summary)
    else:
        st.warning("Please enter valid text or a URL.")
