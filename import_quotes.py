import json
import sqlite3

DB_PATH = "cigarrdata.db"
JSON_PATH = "quotes_with_authors.json"

def import_quotes():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Ensure the quotes table exists with author field
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS quotes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            quote TEXT UNIQUE NOT NULL,
            author TEXT
        )
    """)

    with open(JSON_PATH, "r", encoding="utf-8") as f:
        quotes = json.load(f)

    imported = 0
    skipped = 0
    for item in quotes:
        quote = item.get("quote", "").strip()
        author = item.get("author", "").strip()
        if not quote:
            continue
        try:
            cursor.execute("INSERT INTO quotes (quote, author) VALUES (?, ?)", (quote, author))
            imported += 1
        except sqlite3.IntegrityError:
            skipped += 1  # Duplicate quote

    conn.commit()
    conn.close()
    print(f"✅ Imported {imported} new quotes. Skipped {skipped} duplicates.")

if __name__ == "__main__":
    import_quotes()
