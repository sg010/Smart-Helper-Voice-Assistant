import sqlite3

# Connect to SQLite database (or create if it doesn't exist)
conn = sqlite3.connect("voice_assistant.db", check_same_thread=False)
cursor = conn.cursor()

# Function to create tables if they don't exist
def create_tables():
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS commands (
            command_id INTEGER PRIMARY KEY AUTOINCREMENT,
            command_text TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS responses (
            response_id INTEGER PRIMARY KEY AUTOINCREMENT,
            command_id INTEGER,
            response_text TEXT NOT NULL,
            response_time DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (command_id) REFERENCES commands(command_id)
        );
    """)
    conn.commit()

# Function to insert a new command
def insert_command(command_text):
    cursor.execute("INSERT INTO commands (command_text) VALUES (?)", (command_text,))
    conn.commit()
    return cursor.lastrowid  # Returns inserted command ID

# Function to insert a response
def insert_response(command_id, response_text):
    cursor.execute("INSERT INTO responses (command_id, response_text) VALUES (?, ?)", (command_id, response_text))
    conn.commit()

# Function to fetch last command
def get_last_command():
    cursor.execute("SELECT command_text FROM commands ORDER BY timestamp DESC LIMIT 1")
    return cursor.fetchone()

# Close database connection
def close_connection():
    conn.close()

# Run table creation when script is executed
if __name__ == "__main__":
    create_tables()
    print("Database tables created successfully.")
