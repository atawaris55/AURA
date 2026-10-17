# AURA — Personal AI Voice Email Agent

AURA converts a spoken Hindi, Hinglish, or English command into a professional English email, confirms it with the user, and sends it through Gmail.

Example: say "HOD ko mail karo ki mera assignment late submit hoga", and AURA transcribes it, drafts a professional email to the HOD, shows it for approval, and sends it on confirmation.

## Architecture

Voice input -> AI brain -> Contact resolution -> Draft and confirm -> Gmail API -> Voice response

## Tech stack

- Speech-to-text: OpenAI Whisper (medium model, local)
- AI brain: Google Gemini API (gemini-3.1-flash-lite)
- Contacts: SQLite
- Email sending: Gmail API (OAuth 2.0)

## Setup

1. Clone the repository and create a virtual environment: python -m venv venv, then venv\Scripts\Activate.ps1

2. Install dependencies: pip install -r requirements.txt. FFmpeg must also be installed separately: winget install ffmpeg

3. Create a .env file in the project root with GEMINI_API_KEY and SENDER_NAME. Get a free Gemini API key from aistudio.google.com

4. Set up Gmail API access: create a project in Google Cloud Console, enable the Gmail API, configure the OAuth consent screen (External, add yourself as a test user), create OAuth credentials (Desktop app type), download as credentials.json, place it in the project root

5. Initialize the contacts database: python contacts/database.py. Edit the contact list inside the script to add your own recipients before running it.

## Running AURA

Run: python main.py

Speak your command when prompted. Review the generated draft, then type yes to send, no or cancel to discard, or describe a change to regenerate the draft before confirming again. The first run will open a browser window to authorize Gmail access.

## Demo video

Full walkthrough of AURA, including the ESP32 hardware flow (button press, OLED status, LEDs) and a real email sent via voice command: [Watch on Google Drive](https://drive.google.com/file/d/1v9jD02TIXfys83RtU6VuQTymNdIU7Pmu/view?usp=sharing)

## Known limitations

## Known limitations

- Hindi and Hinglish speech-to-text accuracy is inconsistent. Whisper sometimes mishears words (for example "kal" as "akal") or mixes Devanagari, Urdu, and Roman scripts in the same transcript. A vocabulary hint improves this but does not fully solve it. The AI brain often compensates for small transcription errors, but a draft should always be reviewed before confirming.
- AURA's responses (success messages, error messages, clarification questions) are text-based in the terminal, not spoken aloud. Text-to-speech output was not implemented in this MVP.
- When AURA needs clarification (for example, a missing recipient or an ambiguous name), it asks a question and stops. The user must run the command again with the missing information rather than answering in the same session.
- Confirmation is given by typing yes, no, or feedback in the terminal, not by voice.
- The AI brain fills in small unstated details (for example, assuming "5 o'clock" means "5:00 PM") when generating a draft. This is intentional, since AURA is designed to work from brief spoken context, but it makes the confirmation step before sending important.
- There is no undo-after-send feature. Once "yes" is confirmed, the email sends immediately. Gmail's own "Undo Send" window (10-30 seconds) can be used manually if needed.
- The contact database is a fixed local SQLite file with manually added contacts. There is no voice-based way to add a new contact yet.
- The OAuth app is in Google's "Testing" mode, which limits it to pre-approved test users and requires reauthorization roughly every 7 days.
- The ESP32 hardware layer (Part 8) is a separate, optional stretch goal and is not required for the MVP to function.