from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from backend.musicgen_service import GenerationRequest, MusicGenService

app = FastAPI(title="MusicGen Web Studio")
service = MusicGenService()


class GeneratePayload(BaseModel):
    prompt: str = Field(..., min_length=3, max_length=400)
    genre: str = Field(..., min_length=1, max_length=100)
    mood: str = Field(..., min_length=1, max_length=100)
    tempo: str = Field(..., min_length=1, max_length=20)
    duration_seconds: int = Field(..., ge=5, le=30)


app.mount("/static", StaticFiles(directory="frontend"), name="static")


@app.get("/", response_class=HTMLResponse)
def index() -> HTMLResponse:
    with open("frontend/index.html", "r", encoding="utf-8") as handle:
        return HTMLResponse(handle.read())


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "model": service.model_name, "device": service.device}


@app.post("/api/generate")
def generate(payload: GeneratePayload) -> Response:
    request = GenerationRequest(
        prompt=payload.prompt,
        genre=payload.genre,
        mood=payload.mood,
        tempo=payload.tempo,
        duration_seconds=payload.duration_seconds,
    )
    try:
        audio_bytes, sample_rate = service.generate(request)
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    return Response(
        content=audio_bytes,
        media_type="audio/wav",
        headers={"X-Sample-Rate": str(sample_rate)},
    )
