import hmac, hashlib, subprocess, os
from flask import Flask, request, abort, jsonify

app = Flask(__name__)
WEBHOOK_SECRET = os.environ.get("WEBHOOK_SECRET", "my-secret-key").encode()
DEPLOY_SCRIPT  = os.path.join(os.path.dirname(__file__), "..", "deploy.sh")

def verify_signature(payload, signature):
    mac = hmac.new(WEBHOOK_SECRET, msg=payload, digestmod=hashlib.sha256)
    return hmac.compare_digest("sha256=" + mac.hexdigest(), signature)

@app.route("/webhook", methods=["POST"])
def webhook():
    if not verify_signature(request.data, request.headers.get("X-Hub-Signature-256", "")):
        abort(403)
    payload = request.get_json(silent=True) or {}
    if request.headers.get("X-GitHub-Event") == "push" and payload.get("ref") == "refs/heads/main":
        result = subprocess.run(["bash", DEPLOY_SCRIPT], capture_output=True, text=True)
        print(result.stdout)
        return jsonify({"status": "deployed"}), 200
    return jsonify({"status": "ignored"}), 200

if __name__ == "__main__":
    print("🎧 Webhook listener on port 5001...")
    app.run(host="0.0.0.0", port=5001)