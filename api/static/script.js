const statusData = {
  "rizz": {
    image: "/static/images/rizz.gif",
    audio: "/static/audio/rizz.mp3",
  },
  "bro zone": {
    image: "/static/images/brozone.gif",
    audio: "/static/audio/brozone.mp3",
  },
  "cooked": {
    image: "/static/images/cooked.gif",
    audio: "/static/audio/cooked.mp3",
  },
  "maybe-maybe": {
    image: "/static/images/maybe.gif",
    audio: "/static/audio/maybe.mp3",
  },
  "marry her": {
    image: "/static/images/marryher.gif",
    audio: "/static/audio/marryher.mp3",
  },
  
};

async function analyzeCrush() {
  const text = document.getElementById("crushText").value.trim();
  const result = document.getElementById("result");
  const img = document.getElementById("statusImage");
  const audio = document.getElementById("statusAudio");

  if (!text) {
    result.textContent = "Please enter some chat text!";
    img.style.display = "none";
    audio.pause();
    audio.style.display = "none";
    return;
  }

  result.textContent = "Analyzing...";
  img.style.display = "none";
  audio.pause();
  audio.style.display = "none";

  try {
    const response = await fetch("/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text }),
    });

    const data = await response.json();

    if (data.error) {
      result.textContent = "Error: " + data.error;
      img.style.display = "none";
      audio.pause();
      audio.style.display = "none";
      return;
    }

    const label = data.label.toLowerCase();
    const explanation = data.explanation || "";
    result.textContent = `${label.charAt(0).toUpperCase() + label.slice(1)} — ${explanation}`;

    if (statusData[label]) {
      img.src = statusData[label].image;
      img.style.display = "block";

      audio.src = statusData[label].audio;
      audio.style.display = "block";
      audio.play().catch((e) => {
        console.warn("Audio play was prevented:", e);
      });
    } else {
      img.style.display = "none";
      audio.pause();
      audio.style.display = "none";
    }
  } catch (error) {
    result.textContent = "Network error. Please try again.";
    img.style.display = "none";
    audio.pause();
    audio.style.display = "none";
    console.error(error);
  }
}
