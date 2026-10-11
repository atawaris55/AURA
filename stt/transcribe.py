import whisper

model = whisper.load_model("medium")

NO_SPEECH_THRESHOLD = 0.6

VOCAB_HINT = (
    "Mail करो, message भेजो। HOD, Mentor, Sir, Rahul। "
    "कल, आज, assignment, meeting, project, leave, submit।"
)


def transcribe(audio_path="input.wav"):
    print("Processing...")
    result = model.transcribe(audio_path, fp16=False, initial_prompt=VOCAB_HINT)

    kept = [
        segment["text"]
        for segment in result["segments"]
        if segment["no_speech_prob"] < NO_SPEECH_THRESHOLD
    ]
    return " ".join(kept).strip()


if __name__ == "__main__":
    text = transcribe()
    print("Transcribed:", text)