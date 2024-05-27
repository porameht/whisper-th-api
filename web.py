import streamlit as st
import requests
import soundfile as sf
import numpy as np
from st_audiorec import st_audiorec
import os

st.title("Whisper Small Thai")
st.write("Record an audio file to transcribe:")

# Record audio using st_audiorec
wav_audio_data = st_audiorec()

if wav_audio_data is not None:
    # Play back the recorded audio
    st.audio(wav_audio_data, format='audio/wav')

    # Save the recorded audio to a temporary WAV file
    temp_wav_path = 'audio_temp.wav'
    with open(temp_wav_path, 'wb') as f:
        f.write(wav_audio_data)

    # Upload the audio file to the FastAPI server
    with open(temp_wav_path, 'rb') as f:
        audio_bytes = f.read()
        with st.spinner('🧠 Thinking...'):
            files = {"file": ("audio.wav", audio_bytes, "audio/wav")}
            response = requests.post("http://127.0.0.1:8000/transcribe/", files=files)

            if response.status_code == 200:
                transcription = response.json().get("text", "Transcription failed.")
                st.write(f"Robot Command 🤖: {transcription}")
            else:
                st.error("Failed to transcribe the audio. Server returned status code: {}".format(response.status_code))

    # Clean up temporary WAV file
    st.write("Cleaning up temporary files...")
    try:
        os.remove(temp_wav_path)
    except Exception as e:
        st.error("Error while cleaning up temporary files: {}".format(e))
