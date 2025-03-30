from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker


class ActionSessionStart(Action):
    def name(self) -> Text:
        return "action_session_start"

    async def run(
        self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(
            text="Welcome to Annadata. \n Commands: list goods, login, register, buy history"
        )
