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
    return whisper.load_model('large', device="cpu")
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

languages = {"Hindi": "hi", "English": "en","Spanish": "es", "French": "fr", "Arabic": "ar"}

source_lang = st.selectbox("Source Language", list(languages.keys()))
target_lang = st.selectbox("Target Language", list(languages.keys()))

source_code = languages[source_lang]
target_code = languages[target_lang]
try:
    import torch
    torch.cuda.empty_cache()
    
    if audio_path and st.button('Translate'):
        model = load_model()
        with st.spinner("Transcribing..."):
            # Transcription
            result = model.transcribe(
                audio_path,
                task="transcribe",
                beam_size = 1,
                best_of = 1,
                without_timestamps=True,
                language= source_code
            )

        os.remove(audio_path)
        # Translation part (translating to target language!)
        with st.spinner("Translating..."):
                text = GoogleTranslator(
                    source=source_code,
                    target= target_code
                ).translate(result['text'])

        st.success("Done!")

        st.markdown(f"""
    **Original ({source_lang}):**  
    {result['text']}

    **Tranlated {target_lang}:**  
    {text}
    """)

except Exception as e:
     st.error(f"Failed to do the translation! {str(e)}")