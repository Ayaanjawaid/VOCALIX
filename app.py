import streamlit as st
import pyttsx3
from io import BytesIO

st.set_page_config(page_title="VOCALIX", page_icon=":speaker:")

# Initialize the TTS engine
engine = pyttsx3.init(driverName='sapi5')

# Get available voices
voices = engine.getProperty('voices')

# Streamlit interface
st.title("VOCALIX: Text-to-Speech Converter")

# Select voice
voice_options = {voice.name: voice.id for voice in voices}
selected_voice = st.selectbox("Choose a Voice", list(voice_options.keys()))

# Set the selected voice
engine.setProperty('voice', voice_options[selected_voice])

# Adjust voice speed
speed = st.slider("Select Voice Speed (Words per Minute)", min_value=100, max_value=300, value=200)
engine.setProperty('rate', speed)

# Input text for conversion
text = st.text_area("Enter the text you want to convert to speech:")

# Convert to speech and download
if st.button("Convert to Speech"):
    if text:
        # Create an in-memory file-like object
        audio_file = BytesIO()
        engine.save_to_file(text, 'output.mp3')
        engine.runAndWait()

        # Read the saved file into the BytesIO object
        with open('output.mp3', 'rb') as f:
            audio_file.write(f.read())
        audio_file.seek(0)

        # Play the audio file
        st.audio(audio_file, format='audio/mp3')

        # Download the audio file
        st.download_button(label="Download Audio", data=audio_file, file_name="speech.mp3", mime="audio/mp3")
        st.success("Text converted to speech successfully!")
    else:
        st.warning("Please enter some text.")
