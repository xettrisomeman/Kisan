from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from config import SHOW_HISTORY_URL
import httpx


class ActionShowHistory(Action):
    def name(self) -> str:
        return "action_show_history"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[str, Any]
    ) -> List[Dict[Text, Any]]:
        email = tracker.get_slot("add_user_email_login")
        response = httpx.get(SHOW_HISTORY_URL, params={"email": email})

        if response.status_code == 200 and response.json():
            histories = response.json()
            messages = [
                f"Cancelled Buy Request of {h['good_name']}"
                if h["name"] == "Cancelled Buy Request"
                else f"Buy Order Accepted by {h['seller_email']}"
                if h["name"] == "Buy Order Accepted"
                else f"Accepted Buy Order for {h['good_name']}"
                if h["name"] == "Accepted Buy Order"
                else f"Sent Buy Order to {h['seller_email']}"
                if h["name"] == "Sent Buy Order"
                else None
                if h["name"] == "Good Added"
                else f"{h['good_name']} added"
                if h["name"] == "Good Edited"
                else f"{h['good_name']} edited."
                if h["name"] == "Good Deleted"
                else f"{h['good_name']} deleted."
                for h in histories
            ]
            if len(messages) > 1:
                dispatcher.utter_message(text="\n".join(filter(None, messages)))
        else:
            dispatcher.utter_message(text="No recent activities.")

        return []
