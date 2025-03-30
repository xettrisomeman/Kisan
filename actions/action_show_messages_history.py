from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


json_path = "./database/ask_expert.json"

from utils import retrieve_json_list, find_item_by_key


class ActionShowMessagesHistory(Action):
    def name(self) -> str:
        return "action_show_messages_history"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[str, Any]
    ) -> List[Dict[Text, Any]]:
        email = tracker.get_slot("add_user_email_login")

        data = retrieve_json_list(filename=json_path)
        if data:
            results = find_item_by_key(data, key="email", value=email)
            if results:
                for user_data in results:
                    if user_data.get("email") == email:
                        messages = user_data.get("messages", [])
                        responses = user_data.get("response", "<No Messages>")
                        ai_responses = user_data.get("ai_response", [])
                        dispatcher.utter_message(
                            text=(
                                f"Message: {messages}\n"
                                f"Expert Response: {responses}\n"
                                f"AI Response: {ai_responses}\n\n"
                            )
                        )
            else:
                dispatcher.utter_message(text="You have no messages history.")
        else:
            dispatcher.utter_message(text="You have no messages history.")
