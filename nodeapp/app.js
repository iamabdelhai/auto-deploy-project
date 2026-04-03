const http = require("http");

const VERSION = "2.0.0";

const server = http.createServer((req, res) => {
  res.writeHead(200, { "Content-Type": "text/plain" });
  res.end(`✅ Hello! Version: ${VERSION}\n`);
});

server.listen(3000, () => {
  console.log(`🚀 App running on http://localhost:3000 — v${VERSION}`);
});