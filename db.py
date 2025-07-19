import sqlite3
import string
import random

def init_db() -> None:
    """Initialize the database with urls table and index"""

    # First try to create the database and its cells
    try:
        # Connects with the urls.db database. If one doesn't exists, it creates one
        conn = sqlite3.connect('urls.db')
        # The cursor is created to execute SQL commands
        cursor = conn.cursor()
        # Creates a table with two columns, short_id and input_url. The first is a primary key (unique value), and the second is is just a text
        # field to store the original url, inputed by the user
        cursor.execute('''CREATE TABLE IF NOT EXISTS urls 
                     (short_id TEXT PRIMARY KEY, input_url TEXT)''')
        # This just creates an index on the short_id column to make things faster
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_short_id ON urls (short_id)")
        # Saves all changes to the database
        conn.commit()

    # If any error happens in the way, it catches the error and prints it
    except sqlite3.Error as e:
        print(f"Database initialization error: {e}")

    # CLoses the database, no matter what happens
    finally:
        conn.close()

# This is going to create the ids used for the shortened URLs. You can specify a length, but if not, by default, it is set to 6.
def generate_short_id(length: int=6) -> str:
    """Generate a random short ID"""
    characters = string.ascii_letters + string.digits # The characters variable will be all lowercase letters, all uppercase letters, and all numbers
    return ''.join(random.choice(characters) for _ in range(length)) # It chooses 'length' amount of times a random character from the characters variable and returns a single string

# This function is to prevent duplicating URLs.
def short_id_exists(short_id: str) -> bool:
    """Check if a short ID exists in the database"""
    try:
        conn = sqlite3.connect('urls.db')
        cursor = conn.cursor()
        # This is going to search for short_id in the database
        cursor.execute("SELECT short_id FROM urls WHERE short_id = ?", (short_id,))
        result = cursor.fetchone()
        conn.close()
        # If there is a short_id in the database, it returns True, otherwise returns False.
        return result is not None
    # If any error happens, it returns False. 
    except sqlite3.Error:
        return False