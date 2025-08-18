from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import sqlite3

class ActionSaveApplication(Action):
    def name(self) -> Text:
        return "action_save_application"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        internship = tracker.get_slot("internship_name")
        user_name = tracker.get_slot("user_name")
        email = tracker.get_slot("email")

        conn = sqlite3.connect("applications.db")
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                internship TEXT,
                name TEXT,
                email TEXT
            )
        """)
        cursor.execute("INSERT INTO applications (internship, name, email) VALUES (?, ?, ?)",
                       (internship, user_name, email))
        conn.commit()
        conn.close()

        dispatcher.utter_message(text="Your application has been saved. We'll contact you soon!")
        return []
