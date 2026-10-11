from stt.record import record_audio
from stt.transcribe import transcribe
from brain.email_flow import run_flow


def main():
    audio_file = record_audio(duration=8)
    text = transcribe(audio_file)
    print("Transcript:", text)

    if not text.strip():
        print("I could not hear anything. Please try again.")
        return

    run_flow(text)


if __name__ == "__main__":
    main()