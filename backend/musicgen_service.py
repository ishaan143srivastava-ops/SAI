from __future__ import annotations

import io
import os
from dataclasses import dataclass
from typing import Tuple

import torch
import torchaudio
from audiocraft.models import MusicGen


@dataclass
class GenerationRequest:
    prompt: str
    genre: str
    mood: str
    tempo: str
    duration_seconds: int

    def to_description(self) -> str:
        details = [self.prompt, f"Genre: {self.genre}", f"Mood: {self.mood}", f"Tempo: {self.tempo}"]
        return ", ".join(details)


class MusicGenService:
    def __init__(self) -> None:
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model_name = os.getenv("MUSICGEN_MODEL", "facebook/musicgen-small")
        self.model: MusicGen | None = None

    def load(self) -> None:
        if self.model is None:
            self.model = MusicGen.get_pretrained(self.model_name, device=self.device)

    def generate(self, request: GenerationRequest) -> Tuple[bytes, int]:
        self.load()
        if self.model is None:
            raise RuntimeError("MusicGen model failed to load.")

        duration = max(5, min(30, request.duration_seconds))
        self.model.set_generation_params(duration=duration)
        description = request.to_description()
        with torch.no_grad():
            wav = self.model.generate([description])[0].cpu()

        buffer = io.BytesIO()
        torchaudio.save(buffer, wav, self.model.sample_rate, format="wav")
        buffer.seek(0)
        return buffer.read(), self.model.sample_rate
