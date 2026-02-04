import streamlit as st
import tempfile
import os
import whisper
from deep_translator import GoogleTranslator


st.title("Voice Message Translator")

audio_file = st.file_uploader("Upload audio", type=["mp3", "wav", "m4a"])

@st.cache_resource
def load_model():
    return whisper.load_model('large')
if audio_file:
    st.audio(audio_file)

    if st.button("Translate"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(audio_file.read())
            audio_path = tmp.name
        model = load_model()
        with st.spinner("Transcribing..."):
      
            #  Hindi transcription
            hindi_result = model.transcribe(
                audio_path,
                task="transcribe",
                language="hi"
            )

        os.remove(audio_path)

        with st.spinner("Translating..."):
                english_text = GoogleTranslator(
                    source="hi",
                    target="en"
                ).translate(hindi_result['text'])

        st.success("Done!")

        st.markdown(f"""
**Original (Hindi):**  
{hindi_result['text']}

**English:**  
{english_text}
""")
