from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher


class CheckLoggedIn(Action):
    def name(self) -> str:
        return "check_logged_in"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[str, Any]
    ) -> List[Dict[Text, Any]]:
        logged_in = tracker.get_slot("logged_in")
        if logged_in:
            return [SlotSet("logged_in", True)]
        else:
            return [SlotSet("logged_in", False)]
