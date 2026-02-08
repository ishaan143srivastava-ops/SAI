# MusicGen Web Studio

A fully working, free-stack music generation platform powered by Meta's MusicGen model. It provides a clean web UI to create short music clips from text prompts, control genre/mood/tempo, and play or download the audio.

## Architecture overview

- **Frontend**: HTML/CSS/JavaScript served as static files by FastAPI.
- **Backend**: FastAPI handles requests, validates input, and calls MusicGen.
- **Model**: Meta MusicGen via the official `audiocraft` package (CPU friendly, GPU optional).
- **Audio**: Generated audio is returned as WAV bytes using `torchaudio`.

```
Browser
  ↓ (JSON)
FastAPI (/api/generate)
  ↓
MusicGen (audiocraft)
  ↓
WAV bytes → Browser player + download
```

## Folder structure

```
.
├── backend
│   ├── __init__.py
│   ├── app.py
│   ├── generate_sample.py
│   └── musicgen_service.py
├── frontend
│   ├── app.js
│   ├── index.html
│   └── styles.css
├── output
├── requirements.txt
└── README.md
```

## Environment setup

- Python **3.10+** recommended.
- CPU-only is supported. GPU is optional (CUDA will be used automatically if available).

```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### Optional: change model size

The default is `facebook/musicgen-small` for faster CPU generation. You can pick another model:

```bash
export MUSICGEN_MODEL=facebook/musicgen-medium
```

## Run the backend + frontend

```bash
uvicorn backend.app:app --host 0.0.0.0 --port 8000
```

Open `http://localhost:8000` in your browser.

## Generate a test song (required validation)

This generates the requested test prompt and saves it to `output/test_song.wav`.

```bash
python -m backend.generate_sample
```

## API reference

### `POST /api/generate`

**Body**

```json
{
  "prompt": "string",
  "genre": "string",
  "mood": "string",
  "tempo": "slow | medium | fast",
  "duration_seconds": 5
}
```

**Response**

- WAV audio bytes (`audio/wav`)

## Common errors + fixes

- **Model download is slow**: The first run downloads weights. Give it a few minutes.
- **Out of memory on CPU**: Use `facebook/musicgen-small` and keep durations at 5-10s.
- **Torch/torchaudio mismatch**: Make sure both versions match the ones in `requirements.txt`.
- **Port already in use**: Change the port: `--port 8001`.

## Final checklist

- [x] Backend and frontend are connected.
- [x] Text prompt, genre, mood, tempo, duration controls exist.
- [x] Audio plays in browser and is downloadable as WAV.
- [x] Test song generation script runs locally.
- [x] CPU-friendly defaults in place.
