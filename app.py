import os
from flask import Flask, jsonify, request

from lmstudio_client import LMStudioClient

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False

client = LMStudioClient(
    base_url=os.getenv("LMSTUDIO_BASE_URL", "http://localhost:1234/v1"),
    api_key=os.getenv("LMSTUDIO_API_KEY", "lm-studio"),
    model=os.getenv("LMSTUDIO_MODEL", "local-model"),
)


@app.get("/api/health")
def health():
    return jsonify({
        "ok": True,
        "status": "ready",
        "base_url": client.base_url,
        "model": client.model,
    })


@app.post("/api/ask")
def ask():
    payload = request.get_json(silent=True) or {}
    prompt = payload.get("prompt") or payload.get("message") or ""

    if not prompt:
        return jsonify({"ok": False, "error": "prompt is required"}), 400

    model = payload.get("model") or client.model
    temperature = float(payload.get("temperature", 0.0))
    max_tokens = int(payload.get("max_tokens", 512))

    try:
        response = client.ask(prompt, model=model, temperature=temperature, max_tokens=max_tokens)
        return jsonify({
            "ok": True,
            "model": model,
            "response": response,
        })
    except Exception as exc:  # pragma: no cover - useful for local debugging
        return jsonify({
            "ok": False,
            "error": str(exc),
            "model": model,
        }), 500


if __name__ == "__main__":
    host = os.getenv("FLASK_HOST", "0.0.0.0")
    port = int(os.getenv("FLASK_PORT", "5000"))
    app.run(host=host, port=port, debug=False)
