import sqlite3

def create_tables():
    with sqlite3.connect('aixy.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            said TEXT NOT NULL,
            response TEXT,
            timestamp TEXT DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        conn.commit()

def insertConversation(said, response):
    with sqlite3.connect('aixy.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO conversations (said, response)
            VALUES (?, ?)
        ''', (said, response))
        conn.commit()

def getConversations():
    with sqlite3.connect('aixy.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT said, response, timestamp FROM conversations")
        conversations = cursor.fetchall()
    return conversations

def getLastConversation():
    with sqlite3.connect('aixy.db') as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT said, response, timestamp 
            FROM conversations 
            ORDER BY timestamp DESC 
            LIMIT 1
        """)
        conversation = cursor.fetchone()
    return conversation if conversation else ""

create_tables()