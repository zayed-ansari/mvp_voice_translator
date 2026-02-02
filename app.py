import streamlit as st
import whisper
import os

st.title("Voice Message Translator")
st.write("Upload an audio file to transcribe")

# Upload audio file
audio_file = st.file_uploader("Choose an audio file", type=["mp3", "wav", "m4a"])

if audio_file is not None:
    st.audio(audio_file)
    
    if st.button("Transcribe"):
        with st.spinner("Transcribing..."):
            file_ext = audio_file.name.split(".")[-1]
            temp_file = 'a'
            # Save uploaded file temporarily
            with open("temp_audio.wav", "wb") as f:
                f.write(audio_file.getbuffer())
            
            # Load Whisper model (using 'base' for speed)
            model = whisper.load_model("base")
            
            # Transcribe
            result = model.transcribe("temp_audio.wav",
                                      language="en",
                                      task= "transcribe",
                                      fp16=False)
            
            st.success("Transcription complete!")
            st.write("**Original Text:**")
            st.write(result["text"])
            
            # Clean up
            os.remove("temp_audio.wav")
