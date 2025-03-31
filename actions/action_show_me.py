from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from config import CURRENT_USER_URL
import httpx


class ActionShowMe(Action):
    def name(self) -> str:
        return "action_show_me"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[str, Any]
    ) -> List[Dict[Text, Any]]:
        logged_in = tracker.get_slot("logged_in")
        if logged_in:
            email = tracker.get_slot("add_user_email_login")
            response = httpx.get(CURRENT_USER_URL, params={"email": email}).json()
            dispatcher.utter_message(
                text=(
                    f"Name: {response['users']['name']}\n"
                    f"Email Address: {response['users']['email']}\n"
                    f"Location: {response['users']['location']}\n"
                    f"Interests: {response['users']['interests']}\n"
                )
            )
            if response["bought"]:
                length = len(response["bought"])
                dispatcher.utter_message(text=(f"Goods bought: {length}"))
            else:
                dispatcher.utter_message(text="Goods Bought: None")

            if response["sold"]:
                length = len(response["sold"])
                dispatcher.utter_message(text=f"Goods solds: {length}")
            else:
                dispatcher.utter_message(text="Goods Sold: None")

        else:
            dispatcher.utter_message(text="You are not logged in.")
