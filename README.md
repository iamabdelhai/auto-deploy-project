#  Auto Deployment via GitHub Webhooks

Automatically deploy a Node.js application on every `git push` to `main` using **GitHub Webhooks** + **Python Flask**.

---

##  Project Overview

This project demonstrates a lightweight CI/CD pipeline without any external CI tools.
When a developer pushes code to the `main` branch, GitHub sends an HTTP POST request (Webhook) to a local Flask server, which then triggers a shell script that pulls the latest code and restarts the Node.js app automatically.

```
git push → GitHub → Webhook POST → Flask Listener → deploy.sh → Node.js restarted ✅
```

---
## 📸 Screenshots

### Flask Listener Running
![Flask](screenshots/flask-running.png)

### ngrok Tunnel
![ngrok](screenshots/ngrok-running.png)

### GitHub Webhook
![Webhook](screenshots/github-webhook.png)

### Auto Deploy Result
![Deploy](screenshots/deploy-result.png)

## Tech Stack

| Tool | Role |
|------|------|
| Node.js | Application being deployed |
| Python + Flask | Webhook listener server |
| GitHub Webhooks | Triggers deployment on push |
| ngrok | Exposes localhost to the internet (for local development) |
| Bash | Deploy automation script |

---

## Project Structure

```
auto-deploy-project/
├── nodeapp/
│   ├── app.js              # Node.js HTTP server
│   └── package.json
├── webhook/
│   ├── webhook_server.py   # Flask webhook listener
│   └── requirements.txt
├── deploy.sh               # Automated deploy script
└── README.md
```

---

##  Setup & Usage

### Prerequisites
Make sure these are installed:
```bash
node --version
python3 --version
git --version
```

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/auto-deploy-project.git
cd auto-deploy-project
chmod +x deploy.sh
```

### 2. Start the Node.js App
```bash
cd nodeapp
node app.js
# App running on http://localhost:3000
```

### 3. Start Flask Webhook Listener
```bash
cd webhook
python3 -m pip install flask
export WEBHOOK_SECRET="my-secret-key"
python3 webhook_server.py
# Listening on port 5001...
```

### 4. Expose Port with ngrok
```bash
# In the folder containing ngrok.exe (Windows)
.\ngrok config add-authtoken YOUR_NGROK_TOKEN
.\ngrok http 5001
# Copy the Forwarding URL: https://xxxx.ngrok-free.dev
```

### 5. Configure GitHub Webhook
```
GitHub Repo → Settings → Webhooks → Add webhook

Payload URL  : https://xxxx.ngrok-free.dev/webhook
Content type : application/json
Secret       : my-secret-key
Events       : Just the push event ✅
```

### 6. Test Auto Deployment
```bash
# Edit nodeapp/app.js — change VERSION to "2.0.0"
git add .
git commit -m "bump version to 2.0.0"
git push origin main
# Flask receives the webhook → deploy.sh runs → app restarts automatically
```

Visit `http://localhost:3000` — you should see the new version live.

---

##  Security

- Webhook requests are verified using **HMAC SHA-256 signature** (`X-Hub-Signature-256`)
- The secret is passed via environment variable, never hardcoded
- `hmac.compare_digest()` is used to prevent timing attacks
- `set -e` in deploy.sh stops execution immediately on any error

---

## Errors Encountered & Fixes

These are real errors faced during setup on **Windows with Git Bash / PowerShell**.

---

### Error 1 — `webhook_server.py: No such file or directory`
**Cause:** Running `python3 webhook_server.py` from the root project folder instead of the `webhook/` subfolder.

**Fix:**
```bash
cd webhook
python3 webhook_server.py
```

---

### Error 2 — `ModuleNotFoundError: No module named 'flask'`
**Cause:** Flask was not installed for the Python version being used.

**Fix:**
```bash
# Standard pip install did not work due to Python path mismatch
# Solution: use python3 -m pip to ensure correct Python is targeted
python3 -m pip install flask
```

---

### Error 3 — `ngrok: is not recognized as a command`
**Cause 1:** Running `ngrok` from `C:\Windows\System32` instead of the folder containing `ngrok.exe`.

**Fix:** Open Terminal directly inside the folder containing `ngrok.exe` (right-click → Open in Terminal).

**Cause 2:** On PowerShell, running `ngrok` without `.\` prefix.

**Fix:**
```powershell
# PowerShell requires .\ prefix for local executables
.\ngrok config add-authtoken YOUR_TOKEN
.\ngrok http 5001
```

---

###  Error 4 — GitHub Webhook returned `404`
**Cause:** The Payload URL was set to the example placeholder `abc123.ngrok-free.app` instead of the real ngrok URL, and was also missing `/webhook` at the end.

**Fix:** Copy the exact Forwarding URL from the ngrok terminal and append `/webhook`:
```
https://merle-comely-clarita.ngrok-free.dev/webhook
```

---

## 📊 How It Works — Full Flow

```
1. Developer runs: git push origin main
2. GitHub detects the push event
3. GitHub sends HTTP POST to /webhook (ngrok URL)
4. ngrok forwards the request to Flask on localhost:5001
5. Flask verifies the HMAC SHA-256 signature
6. Flask checks that ref == "refs/heads/main"
7. Flask runs deploy.sh
8. deploy.sh:
     a. git pull origin main
     b. npm install --production
     c. pkill -f "node app.js"  (stop old instance)
     d. nohup node app.js &     (start new instance)
9. App is live with the latest code ✅
```

---

## 🔮 Future Improvements

- Add **Telegram or Slack notifications** after each deployment
- Add a **rollback script** triggered on deploy failure
- Replace `nohup` with **PM2** for production-grade process management
- Containerize with **Docker** and use `docker compose up -d --build`
- Migrate the webhook listener to **Jenkins** for a full CI/CD pipeline

---

— [@iamabdelhai](https://github.com/iamabdelhai)
