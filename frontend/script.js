async function fetchReels() {
  const mood = document.getElementById("moodInput").value;
  const output = document.getElementById("output");
  output.innerHTML = "Loading...";

  try {
    const res = await fetch(`https://your-backend-url.onrender.com/api/reels?mood=${mood}`);
    const data = await res.json();
    output.innerHTML = "";

    if (Array.isArray(data)) {
      // General interaction message
      const moodNice = mood.charAt(0).toUpperCase() + mood.slice(1);
      output.innerHTML += `<p>Hey! You're in the mood for something <strong>${moodNice}</strong>? Great choice! Here are some reels for you 🎬</p>`;

      // Show video links
      data.forEach(url => {
        output.innerHTML += `<a href="${url}" target="_blank">${url}</a>`;
      });
    } else {
      output.innerHTML = `<p>😕 Oops! I don't have reels for that mood yet. Try romantic, cozy, funny, or adventure!</p>`;
    }
  } catch (err) {
    output.innerHTML = "<p>❌ Something went wrong. Please try again later.</p>";
  }
}
