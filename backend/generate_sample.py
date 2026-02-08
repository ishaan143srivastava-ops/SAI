from __future__ import annotations

from pathlib import Path

from backend.musicgen_service import GenerationRequest, MusicGenService

OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)


def main() -> None:
    service = MusicGenService()
    request = GenerationRequest(
        prompt="Dark melodic hip-hop beat with emotional piano and slow drums",
        genre="hip-hop",
        mood="emotional",
        tempo="slow",
        duration_seconds=5,
    )
    audio_bytes, sample_rate = service.generate(request)

    output_path = OUTPUT_DIR / "test_song.wav"
    output_path.write_bytes(audio_bytes)
    print(f"Saved to {output_path} at {sample_rate} Hz")


if __name__ == "__main__":
    main()
