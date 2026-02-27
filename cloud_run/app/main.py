import os

from flask import Flask, jsonify, render_template, request
from google import genai

app = Flask(__name__)

# ── Configuration ────────────────────────────────────────────
PROJECT_ID = os.environ.get("PROJECT_ID", "statg529300220261-01d2")
LOCATION = "global"
MODEL_ID = "gemini-3.1-pro-preview"

# Initialize the Vertex AI client once at startup
client = genai.Client(vertexai=True, project=PROJECT_ID, location=LOCATION)


@app.route("/")
def index():
    """Serve the chat web UI."""
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    """Send a user message to Gemini and return the response."""
    data = request.get_json(silent=True) or {}
    message = data.get("message", "").strip()
    if not message:
        return jsonify({"error": "message is required"}), 400

    try:
        response = client.models.generate_content(
            model=MODEL_ID,
            contents=message,
        )
        return jsonify({"reply": response.text})
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=True)
