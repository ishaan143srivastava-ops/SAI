const form = document.getElementById("music-form");
const statusEl = document.getElementById("status");
const player = document.getElementById("player");
const downloadLink = document.getElementById("download");
const generateButton = document.getElementById("generate");

const setStatus = (message) => {
  statusEl.textContent = message;
};

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const prompt = document.getElementById("prompt").value.trim();
  const genre = document.getElementById("genre").value.trim();
  const mood = document.getElementById("mood").value.trim();
  const tempo = document.getElementById("tempo").value;
  const duration = Number(document.getElementById("duration").value);

  if (!prompt) {
    setStatus("Please enter a prompt.");
    return;
  }

  setStatus("Generating... this can take 30-90 seconds on CPU.");
  generateButton.disabled = true;

  try {
    const response = await fetch("/api/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        prompt,
        genre,
        mood,
        tempo,
        duration_seconds: duration,
      }),
    });

    if (!response.ok) {
      const data = await response.json();
      throw new Error(data.detail || "Generation failed");
    }

    const blob = await response.blob();
    const audioUrl = URL.createObjectURL(blob);
    player.src = audioUrl;
    downloadLink.href = audioUrl;
    setStatus("Generation complete. Press play or download the file.");
  } catch (error) {
    setStatus(`Error: ${error.message}`);
  } finally {
    generateButton.disabled = false;
  }
});
