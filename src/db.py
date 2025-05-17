import sqlite3

conection = sqlite3.connect('aixy.db')
cursor = conection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS conversations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    said TEXT NOT NULL,
    response TEXT,
    timestamp TEXT DEFAULT CURRENT_TIMESTAMP
)
''')


def insertConversation(said, response):
    cursor.execute(f'''
    INSERT INTO conversations (said, response)
    VALUES (?, ?)
    ''', (said, response))

    conection.commit()

def getConversations():
    cursor.execute("SELECT said, response, timestamp FROM conversations")
    conversations = cursor.fetchall()
    return conversations

def getLastConversation():
    cursor.execute("""
        SELECT said, response, timestamp 
        FROM conversations 
        ORDER BY timestamp DESC 
        LIMIT 1
    """)
    conversation = cursor.fetchone()
    if conversation:
        return conversation
    else:
        return ""

def closeConnection():
    cursor.close()
    conection.close()