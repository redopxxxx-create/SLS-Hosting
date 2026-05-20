import React from "react";

const projects = [
  { name: "AnimeBot", status: "Running", uptime: "2d 4h", speed: "3.2 MB/s", files: 22 },
  { name: "ZipHost", status: "Queued", uptime: "0h", speed: "0 MB/s", files: 2 },
];

export function App() {
  return (
    <main className="shell">
      <section className="hero">
        <h1>⌈ 🚀 𝐒𝐋𝐒 𝐂𝐋𝐎𝐔𝐃 𝐏𝐀𝐍𝐄𝐋 ⌋</h1>
        <p>Realtime speed • Uptime • File hosting metrics</p>
      </section>
      <section className="stats">
        <div className="chip">⚡ Net Speed: 12.6 MB/s</div>
        <div className="chip">🟢 Uptime: 99.93%</div>
        <div className="chip">💾 Storage: 12.2 / 50 GB</div>
      </section>
      <section className="grid">
        {projects.map((p) => (
          <article key={p.name} className="card">
            <h3>📦 {p.name}</h3>
            <p>🔥 Status: {p.status}</p>
            <p>🕒 Uptime: {p.uptime}</p>
            <p>⚡ Speed: {p.speed}</p>
            <p>📂 Files: {p.files}</p>
            <div className="meter"><span style={{ width: p.status === "Running" ? "84%" : "22%" }} /></div>
          </article>
        ))}
      </section>
    </main>
  );
}
