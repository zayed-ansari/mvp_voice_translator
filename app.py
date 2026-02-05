import streamlit as st
import tempfile
import os
import whisper
from deep_translator import GoogleTranslator
from audiorecorder import audiorecorder
st.title("Voice Message Translator")

audio_file = st.file_uploader("Upload audio", type=["mp3", "wav", "m4a"])
st.subheader("Record Audio")
audio_rec = audiorecorder('Start Recording', 'Stop Recording')
@st.cache_resource
def load_model():
    return whisper.load_model('large')
audio_path = None
if audio_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp:
         tmp.write(audio_file.read())
         audio_path = tmp.name
    st.audio(audio_file)
elif len(audio_rec) > 0:
    with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp:
         audio_rec.export(tmp.name, format='wav')
         audio_path = tmp.name
    st.audio(audio_path)

try:
    if audio_path and st.button('Translate'):
        model = load_model()
        with st.spinner("Transcribing..."):
        
                #  Hindi transcription
            hindi_result = model.transcribe(
                audio_path,
                task="transcribe",
                language="hi"
            )

        os.remove(audio_path)
        # Translation part (translating to english!)
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

except Exception as e:
     st.error(f"Failed to do the translation! {str(e)}")