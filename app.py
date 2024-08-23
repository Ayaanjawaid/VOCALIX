import streamlit as st
from gtts import gTTS
import io
from pydub import AudioSegment
from pydub.playback import play
import base64

st.set_page_config(page_title="VOCALIX", page_icon=":speaker:")

# Function to convert text to speech using gTTS and adjust speed
def text_to_speech(text, lang, speed):
    tts = gTTS(text=text, lang=lang, slow=False)
    audio_file = io.BytesIO()
    tts.write_to_fp(audio_file)
    audio_file.seek(0)

    # Adjusting speed
    audio_file.seek(0)
    audio = AudioSegment.from_mp3(audio_file)
    new_sample_rate = int(audio.frame_rate * speed)
    audio = audio._spawn(audio.raw_data, overrides={'frame_rate': new_sample_rate})
    audio = audio.set_frame_rate(44100)
    adjusted_audio_file = io.BytesIO()
    audio.export(adjusted_audio_file, format="mp3")
    adjusted_audio_file.seek(0)
    return adjusted_audio_file

# Streamlit UI components
st.title("Text to Speech Converter")
text = st.text_area("Enter text here")
lang = st.selectbox("Select Language", ["en", "es", "fr", "de", "ja"])  # Add more languages if needed
speed = st.slider("Select Speed (0.5x - 2x)", min_value=0.5, max_value=2.0, value=1.0, step=0.1)

if st.button("Convert"):
    if text:
        audio_data = text_to_speech(text, lang, speed)
        st.audio(audio_data, format="audio/mp3")

        # Option to download the file
        audio_data.seek(0)
        st.download_button("Download Audio", data=audio_data, file_name="output.mp3", mime="audio/mp3")
    else:
        st.error("Please enter some text.")

