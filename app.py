import streamlit as st
import whisper
import tempfile
import os
st.title("Voice Message Translator")


audio_file = st.file_uploader("Upload audio", type=["mp3", "wav", "m4a"])


# Loading the model- using 'large' model for better results
@st.cache_resource
def load_model():
    return whisper.load_model("large")  

if audio_file:
    st.audio(audio_file)

    if st.button("Translate"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(audio_file.read())
            audio_path = tmp.name

        model = load_model()

        with st.spinner("Processing..."):
            # Hindi transcription
            hindi_result = model.transcribe(
                audio_path,
                task="transcribe",
                language="hi"
            )

            # English translation
            english_result = model.transcribe(
                audio_path,
                task="translate"
            )

        os.remove(audio_path)

        hindi_text = hindi_result["text"].strip()
        english_text = english_result["text"].strip()

        st.success("Done!")

     
        st.markdown(
            f"""
**Original (Hindi):** {hindi_text}  

**English:** {english_text}
"""
        )
