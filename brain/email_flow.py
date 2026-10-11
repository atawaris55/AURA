from brain.intent_parser import parse_intent
from brain.error_handler import get_error_message
from contacts.database import resolve_contact
from gmail.send_email import send_email


def show_draft(parsed):
    print("-" * 40)
    print("Subject:", parsed["subject"])
    print("-" * 40)
    print(parsed["body"])
    print("-" * 40)


def get_user_decision():
    answer = input("Should I send this email? (yes / no, cancel / no, <feedback>): ").strip()
    return answer


def build_draft(user_text):
    parsed = parse_intent(user_text)

    if parsed is None:
        return {"status": "error", "message": "Sorry, something went wrong understanding that request."}

    if parsed["needs_clarification"]:
        return {"status": "clarification", "message": parsed["clarification_question"]}

    contact_result = resolve_contact(parsed["recipient_raw"])

    if contact_result["status"] == "not_found":
        return {"status": "error", "message": contact_result["message"]}

    if contact_result["status"] == "ambiguous":
        return {"status": "error", "message": contact_result["message"]}

    return {"status": "ready", "parsed": parsed, "contact": contact_result}


def send_draft(parsed, contact_result):
    try:
        result = send_email(
            to=contact_result["email"],
            subject=parsed["subject"],
            body=parsed["body"]
        )
        return {"status": "sent", "message_id": result["id"]}
    except Exception as error:
        return {"status": "error", "message": get_error_message(error)}


def run_flow(user_text):
    try:
        parsed = parse_intent(user_text)

        if parsed is None:
            print("Sorry, something went wrong understanding that request.")
            return

        if parsed["needs_clarification"]:
            print("Clarification needed:", parsed["clarification_question"])
            return

        contact_result = resolve_contact(parsed["recipient_raw"])

        if contact_result["status"] == "not_found":
            print(contact_result["message"])
            return

        if contact_result["status"] == "ambiguous":
            print(contact_result["message"])
            return

        print("Recipient:", contact_result["name"], "-", contact_result["email"])

        while True:
            show_draft(parsed)
            decision = get_user_decision().lower()

            if decision in ["yes", "y", "haan", "ha"]:
                result = send_email(
                    to=contact_result["email"],
                    subject=parsed["subject"],
                    body=parsed["body"]
                )
                print("Email sent successfully.")
                print("(Message ID:", result["id"], ")")
                return

            if decision in ["no", "cancel", "no cancel", "mat bhejo"]:
                print("Cancelled by user.")
                return

            feedback_text = f"The user wants to edit the previous email draft. Their instruction: '{decision}'. Original recipient request: '{user_text}'. Regenerate the subject and body accordingly."
            parsed = parse_intent(feedback_text)

    except Exception as error:
        print(get_error_message(error))


if __name__ == "__main__":
    test_input = "HOD ko mail karo ki mera assignment late submit hoga"
    run_flow(test_input)