from flask import Flask
import state
from stt.record import record_audio
from stt.transcribe import transcribe
from brain.email_flow import build_draft, send_draft

app = Flask(__name__)


@app.route("/trigger", methods=["GET"])
def trigger():
    print("Received trigger from ESP32")
    state.status_message = "Listening..."

    audio_file = record_audio(duration=8)
    text = transcribe(audio_file)
    print("Transcript:", text)

    if not text.strip():
        state.status_message = "Could not hear anything"
        state.current_draft = None
        state.current_contact = None
        return "no_speech"

    result = build_draft(text)

    if result["status"] == "ready":
        state.current_draft = result["parsed"]
        state.current_contact = result["contact"]
        state.status_message = "Draft ready: " + result["parsed"]["subject"]
        return "draft_ready"

    state.current_draft = None
    state.current_contact = None
    state.status_message = result["message"]
    return "no_draft"


@app.route("/status", methods=["GET"])
def status():
    return state.status_message


@app.route("/confirm", methods=["GET"])
def confirm():
    if state.current_draft is None:
        state.status_message = "No draft to send"
        return "no_draft"

    result = send_draft(state.current_draft, state.current_contact)

    if result["status"] == "sent":
        state.status_message = "Email sent successfully"
        state.current_draft = None
        state.current_contact = None
        return "sent"

    state.status_message = result["message"]
    return "error"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)