from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from config import SHOW_HISTORY_URL
import httpx


class ActionShowActivities(Action):
    def name(self) -> str:
        return "action_show_activities"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[str, Any]
    ) -> List[Dict[Text, Any]]:
        email = tracker.get_slot("add_user_email_login")
        response = httpx.get(SHOW_HISTORY_URL, params={"email": email})
        if response.status_code == 200:
            histories = response.json()
            messages = ""
            for h in histories:
                messages += f"{h['name']}: {h['good_name']}\n"
            if len(histories) >= 1:
                dispatcher.utter_message(text=messages)
            else:
                dispatcher.utter_message(text="No recent activities.")
