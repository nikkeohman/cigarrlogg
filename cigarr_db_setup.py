# cigarr_db_setup.py
# Körs en gång för att skapa databasen och lägga in citat

import sqlite3

DB_PATH = "cigarrdata.db"
QUOTES = [
    "Sometimes a cigar is just a cigar.",
    "A good cigar is like tasting a good wine: you smell it, you taste it, you look at it, you feel it, you can even hear it.",
    "I have made it a rule never to smoke more than one cigar at a time.",
    "A woman is only a woman, but a good cigar is a smoke.",
    "Cigars are the perfect complement to life's contemplative moments.",
    "A cigar numbs sorrow and fills the solitary hours with a million gracious images.",
    "A cigar is like a port—meant to be enjoyed slowly.",
    "I smoke in moderation. Only one cigar at a time."
    # Lägg till fler citat här eller ladda från fil
]

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Skapa tabeller
cursor.execute("""
CREATE TABLE IF NOT EXISTS quotes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    quote TEXT UNIQUE NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS logg (
    timestamp TEXT NOT NULL,
    temperature REAL NOT NULL,
    humidity REAL NOT NULL,
    quote_id INTEGER,
    FOREIGN KEY (quote_id) REFERENCES quotes(id)
)
""")

# Lägg in citat om de inte redan finns
for quote in QUOTES:
    try:
        cursor.execute("INSERT INTO quotes (quote) VALUES (?)", (quote,))
    except sqlite3.IntegrityError:
        pass  # Skip duplicates

conn.commit()
conn.close()

print("✅ Databas klar och citat importerade.")
