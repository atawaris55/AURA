import os
import json
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
SENDER_NAME = os.getenv("SENDER_NAME", "").strip()

SYSTEM_PROMPT = """You are AURA's intent parser. The user will speak in Hindi, Hinglish, or English asking you to send an email.

Your job: convert their spoken request into a JSON object with EXACTLY this structure, nothing else:

{
  "intent": "send_email",
  "recipient_raw": "<who they mentioned, as spoken>",
  "tone": "professional",
  "subject": "<short email subject>",
  "body": "<full professional English email body>",
  "needs_clarification": false,
  "clarification_question": null
}

Rules:
- Output ONLY valid JSON. No explanation, no markdown, no extra text before or after.
- Always write subject and body in professional English, even if the user spoke in Hindi/Hinglish.
- Default tone is "professional" unless the user explicitly asks for "casual" or "friendly" tone.
- Never invent information the user did not provide.
- If the recipient is missing or the reason/content for the email is missing or too vague, set needs_clarification to true, set subject and body to null, and write a specific clarification_question asking for exactly what is missing.
- Always write recipient_raw in English (Roman) letters, transliterating if the user spoke it in Hindi script. For example, write "Mentor" instead of the Devanagari spelling.
- Never use placeholders such as [Your Name] or [Recipient] anywhere, including the subject.
"""


def build_sender_note():
    if SENDER_NAME:
        return f"The sender's name is {SENDER_NAME}. End the email body with a closing line followed by that name."
    return "The sender's name is unknown. End the email body with a closing line only, and do not add any name."


def parse_intent(user_text):
    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=f"{SYSTEM_PROMPT}\n\n{build_sender_note()}\n\nUser said: \"{user_text}\""
    )
    raw_text = response.text.strip()

    if raw_text.startswith("```"):
        raw_text = raw_text.strip("`")
        raw_text = raw_text.replace("json", "", 1).strip()

    try:
        parsed = json.loads(raw_text)
        return parsed
    except json.JSONDecodeError:
        print("Could not parse JSON. Raw response was:")
        print(raw_text)
        return None


if __name__ == "__main__":
    test_input = "मेंटर को मेल करो कि मैं कल लैब में नहीं आ पाऊँगा"
    result = parse_intent(test_input)
    if result:
        print("Parsed successfully:")
        print(json.dumps(result, indent=2))
        print("Access test - recipient_raw:", result["recipient_raw"])