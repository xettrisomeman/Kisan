from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

import json


json_path = "./database/ask_expert.json"

from utils import ask_ai, save_json_as_list


class ActionAskExpert(Action):
    def name(self) -> str:
        return "action_ask_expert"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[str, Any]
    ) -> List[Dict[Text, Any]]:
        message = tracker.get_slot("message_to_expert")
        if tracker.get_slot("logged_in"):
            email = tracker.get_slot("add_user_email_login")
        else:
            email = tracker.get_slot("collect_email")

        dispatcher.utter_message(
            text="Message has been sent to expert. Wait for 1-2 business day for response."
        )
        ai_res = ask_ai(message=message)
        data = {
            "messages": message,
            "email": email,
            "expert_response": None,
            "ai_response": ai_res,
        }
        save_json_as_list(data=data, filename=json_path)

        dispatcher.utter_message(text=f"Ai Response: \n {ai_res}")
