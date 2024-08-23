import streamlit as st
from gtts import gTTS
import io
import base64

st.set_page_config(page_title="VOCALIX", page_icon=":speaker:")

# Function to convert text to speech using gTTS
def text_to_speech(text, lang, speed):
    tts = gTTS(text=text, lang=lang, slow=False)
    audio_file = io.BytesIO()
    tts.write_to_fp(audio_file)
    audio_file.seek(0)
    return audio_file

# Streamlit UI components
st.title("Text to Speech Converter")
text = st.text_area("Enter text here")
lang = st.selectbox("Select Language", ["en", "es", "fr", "de", "ja"])  # Add more languages if needed

if st.button("Convert"):
    if text:
        audio_data = text_to_speech(text, lang, 1)  # Speed is not directly supported by gTTS
        st.audio(audio_data, format="audio/mp3")

        # Option to download the file
        audio_data.seek(0)
        st.download_button("Download Audio", data=audio_data, file_name="output.mp3", mime="audio/mp3")
    else:
        st.error("Please enter some text.")

