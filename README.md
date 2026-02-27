# Voice Message Translator

Tired of receiving voice messages in languages you don't understand? This tool lets you upload or record audio in one language and get a translation in another — all running locally on your machine, no API costs.

Built with Whisper for transcription and deep-translator for translation. Slapped a Streamlit UI on top so it's actually usable.

---

## What it does

- Upload an audio file (mp3, wav, m4a) or record directly in the browser
- Pick source and target language
- Get the original transcription + translation side by side

Tested with Hindi, Spanish, French, Arabic. Interesting thing I ran into — Whisper sometimes returns Urdu script when you feed it Hindi audio, because they're essentially the same spoken language written differently. Worth knowing if you're working with South Asian audio. But this was on  `medium model`, on `large model` it detected as hindi.

---

## Tech Stack

- [Whisper](https://github.com/openai/whisper) — local speech-to-text, runs fully offline
- [deep-translator](https://github.com/nidhaloff/deep-translator) — handles the translation via Google Translate under the hood
- [Streamlit](https://streamlit.io) — UI
- [streamlit-audiorecorder](https://github.com/Joooohan/audio-recorder-streamlit) — in-browser recording

---

## Model Selection (important)

Whisper comes in different sizes. Which one you use depends on your hardware:

| Model | VRAM needed | Speed | Quality |
|-------|-------------|-------|---------|
| base | ~1 GB | fast | decent |
| small | ~2 GB | fast | good |
| medium | ~3 GB | moderate | great |
| large | ~5+ GB | slow | best |

I have a 4GB GPU so `medium` is the limit for me. If you're running on more VRAM then go for `large`. For me I used `device = "cpu"` — it's slower but gets the job done.

To change the model, edit this line in `app.py`:
```python
return whisper.load_model('base', device = "cuda")  # change to small, medium, or large. But large is recommended
# If you don't have gpu then change device = "cpu"
```

---

## Setup
**Note**:- I'm running cuda 12.5 on my system so I'm using pytorch v2.6
```bash
git clone https://github.com/zayed-ansari/mvp_voice_translator
cd mvp_voice_translator

# CPU (default)
pip install -r requirements.txt

# GPU (CUDA 12.4) — faster transcription
pip install -r requirements-gpu.txt
```

**Requirements:**
```
# For gpu users
streamlit
torch==2.6.0 --index-url https://download.pytorch.org/whl/cu124
torchvision==0.21.0 --index-url https://download.pytorch.org/whl/cu124
torchaudio==2.6.0 --index-url https://download.pytorch.org/whl/cu124
streamlit-audiorecorder
deep-translator
openai-whisper

# For CPU users
streamlit
torch
torchvision
torchaudio
streamlit-audiorecorder
deep-translator
openai-whisper
```

Also needs ffmpeg installed on your system:
```bash
# Ubuntu/Debian
sudo apt install ffmpeg

# Mac
brew install ffmpeg

# Windows
# Download from https://ffmpeg.org/download.html
```

---

## Limitations

- First run downloads the Whisper model (~150MB for base, up to 3GB for large) so give it a minute
- Translation quality depends on Google Translate — it's fine for most languages but not perfect
- Currently supports: Hindi, Spanish, French, Arabic, English. Easy to add more by editing the `languages` dict in `app.py`
- No TTS yet — output is text only

---

## What's next

- Add text-to-speech so you hear the translation, not just read it
- Auto language detection instead of manually selecting source language
- Support for longer audio files (currently works best under 2-3 minutes)