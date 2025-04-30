from ollama import Client
from time import sleep
import sqlite3
import logging
import tank
import llm
import env
import os

movements = {
    "forward": {"direction": "forward", "speed": 2},
    "backward": {"direction": "backward", "speed": 2},
    "slow forward": {"direction": "forward", "speed": 1},
    "slow backward": {"direction": "backward", "speed": 1},
    "fast forward": {"direction": "forward", "speed": 3},
    "fast backward": {"direction": "backward", "speed": 3},
    "faster forward": {"direction": "forward", "speed": 4},
    "left": {"direction": "left", "speed": 2},
    "right": {"direction": "right", "speed": 2},
    "left fast": {"direction": "left", "speed": 3},
    "right fast": {"direction": "right", "speed": 3},
    "left very fast": {"direction": "left", "speed": 4},
    "right very fast": {"direction": "right", "speed": 4},
    "left hiper fast": {"direction": "left", "speed": 4},
    "right hiper fast": {"direction": "right", "speed": 4},
}

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')



def init_conversations_db():
    """
    CONVERSATION MEMORY TABLE (SQLITE DATABASE)
    """
    conn = sqlite3.connect(env.DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS conversations (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        response TEXT,
                        time DATETIME DEFAULT CURRENT_TIMESTAMP
                    )''')
    conn.commit()
    conn.close()



def init_definitions_db():
    """
    MEMORY FILE (SQLITE DATABASE)
    ------------------------------------------------
    |   thing   |   definition   |     category    |
    ------------------------------------------------
    
    categories = [info, visual]
    """
    conn = sqlite3.connect(env.DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS definitions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        thing VARCHAR(255),
                        definition TEXT,
                        category VARCHAR(25))''')
    conn.commit()
    conn.close()


def accessDefinitionMemory(thing, category):
    if category == 'info' or category == 'visual':
        conn = sqlite3.connect(env.DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT definition FROM definitions WHERE (category = ?) AND (thing = ?)", (category, thing))
        data = cursor.fetchall()
        conn.close()
        
        if data:
            for row in data:
                definition = row[0]
            print(definition)
            return definition
        else:
            return None
        
    else:
        logging.warning("Invalid Category!")
        return None

def accessConversationMemory(number_to_return=2):
    pass


def addMemory(thing, definition, category):
    conn = sqlite3.connect(env.DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO definitions (thing, definition, category) VALUES (?, ?, ?)", (thing, definition, category))
    conn.commit()
    conn.close()


def calculatedWaitingTime(low_usage_delay):
    sleep(os.getloadavg()[0] * low_usage_delay)


def drive(direction, intensity):
    Motors = tank.Motor()
    if 'forward' in direction:
        Motors.drive_forward(intensity)
    elif 'backward' in direction:
        Motors.drive_backward(intensity)
    elif 'left' in direction:
        Motors.drive_left(intensity)
    elif 'right' in direction:
        Motors.drive_right(intensity)
    elif 'finded' in direction:
        Clamp = tank.Clamp()
        Clamp.down()
    sleep(0.35)
    Motors.stop()

def verifyObstacules():
    ultrassonic = tank.Ultrasonic()
    Motors = tank.Motor()
    if ultrassonic.get_distance() < 7.5:
        Motors.driveLeft(2)
        sleep(0.2)
    
    Motors.stop()

def getDistance():
    ultrassonic = tank.Ultrasonic()
    return ultrassonic.get_distance()
    

def findObjectVisionPrompt(thing, localization=None, MemoryFile=True, additionalPrompt=None):
    definition = None

    if MemoryFile:
        definition = accessMemory(thing, 'visual')
        
    if definition is None:
        definition = llm.get(env.OLLAMA_LANGUAGE_MODEL, env.OLLAMA_EN_SEARCH_VISUAL_PROMPT + thing)
        addMemory(thing, definition, 'visual')
    
    if additionalPrompt:
        prompt = f"Your main objective is to detect the '{thing}' object and approach it, when you find it you must come face to face with it, with a distance between you of 100mm, in this case you should ignore all other outputs and only provide the word 'finded', without additional explanations. Visual description: {definition}" + "\n\n" + str(additionalPrompt)
    
        if localization is not None:
            prompt = f"Your main objective is to detect the '{thing}' object in the '{localization}' localization and approach it, when you find it you must come face to face with it, with a distance between you of 100mm, in this case you should ignore all other outputs and only provide the word 'finded', without additional explanations. Visual description: {definition}" + "\n\n" + str(additionalPrompt)
    else:
        prompt = f"Your main objective is to detect the '{thing}' object and approach it, when you find it you must come face to face with it, with a distance between you of 100mm, in this case you should ignore all other outputs and only provide the word 'finded', without additional explanations. Visual description: {definition}"
    
        if localization is not None:
            prompt = f"Your main objective is to detect the '{thing}' object in the '{localization}' localization and approach it, when you find it you must come face to face with it, with a distance between you of 100mm, in this case you should ignore all other outputs and only provide the word 'finded', without additional explanations. Visual description: {definition}"
        
    return env.OLLAMA_VISION_DECISION_PROMPT + prompt