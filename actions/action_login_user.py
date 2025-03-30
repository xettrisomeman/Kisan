from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

from config import LOGIN_USER_URL
import httpx


class ActionLoginUser(Action):
    def name(self) -> str:
        return "action_login_user"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[str, Any]
    ) -> List[Dict[Text, Any]]:
        email = tracker.get_slot("add_user_email_login")
        password = tracker.get_slot("add_user_password_login")
        payload = {
            "email": email,
            "password": password,
        }
        response = httpx.post(LOGIN_USER_URL, json=payload)
        if response.status_code == 200:
            return [SlotSet("logged_in", True)]
        else:
            return [SlotSet("logged_in", False)]
