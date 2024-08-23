import pyttsx3
import streamlit as st
import os
import base64

st.set_page_config(page_title="VOCALIX", page_icon=":speaker:")

# Initialize the TTS engine with 'espeak' driver
engine = pyttsx3.init(driverName='espeak')

# Get available voices
voices = engine.getProperty('voices')

# Function to convert text to speech
def text_to_speech(text, voice_id, speed):
    engine.setProperty('voice', voice_id)
    engine.setProperty('rate', speed)
    engine.save_to_file(text, 'output.mp3')
    engine.runAndWait()

    # Read the audio file and encode it for download
    with open('output.mp3', 'rb') as audio_file:
        audio_bytes = audio_file.read()
    os.remove('output.mp3')
    return audio_bytes

# Streamlit UI components
st.title("Text to Speech Converter")
text = st.text_area("Enter text here")
voice = st.selectbox("Select Voice", [(voice.name, voice.id) for voice in voices])
speed = st.slider("Select Speed", min_value=50, max_value=300, value=150)

if st.button("Convert"):
    if text:
        audio_data = text_to_speech(text, voice[1], speed)
        st.audio(audio_data, format="audio/mp3")

        # Option to download the file
        st.download_button("Download Audio", data=audio_data, file_name="output.mp3", mime="audio/mp3")
    else:
        st.error("Please enter some text.")
