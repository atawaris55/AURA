import sqlite3

DB_PATH = "contacts/contacts.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            alias TEXT,
            role TEXT,
            email TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def add_contact(name, alias, role, email):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO contacts (name, alias, role, email) VALUES (?, ?, ?, ?)",
        (name, alias, role, email)
    )
    conn.commit()
    conn.close()

def get_all_contacts():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM contacts")
    rows = cursor.fetchall()
    conn.close()
    return rows
def find_contacts(query):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM contacts WHERE alias LIKE ? OR role LIKE ? OR name LIKE ?",
        (f"%{query}%", f"%{query}%", f"%{query}%")
    )
    rows = cursor.fetchall()
    conn.close()
    return rows
def resolve_contact(query):
    matches = find_contacts(query)

    if len(matches) == 0:
        return {
            "status": "not_found",
            "message": f"I don't have an email saved for '{query}'."
        }

    if len(matches) == 1:
        contact = matches[0]
        return {
            "status": "resolved",
            "email": contact[4],
            "name": contact[1]
        }

    names = [f"{m[1]} ({m[3]})" for m in matches]
    options = " or ".join(names)
    return {
        "status": "ambiguous",
        "message": f"Which one did you mean — {options}?",
        "candidates": matches
    }
if __name__ == "__main__":
    print("Test 1 - 'Sir' (ambiguous):")
    print(resolve_contact("Sir"))

    print("\nTest 2 - 'HOD' (exact):")
    print(resolve_contact("HOD"))

    print("\nTest 3 - 'Unknown Person' (no match):")
    print(resolve_contact("Unknown Person"))