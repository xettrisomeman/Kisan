from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher


import httpx
from config import DELETE_GOOD_URL


class ActionDeleteGood(Action):
    def name(self) -> str:
        return "action_delete_good"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[str, Any]
    ) -> List[Dict[Text, Any]]:
        try:
            idx = tracker.get_slot("which_good_to_show")
            name = httpx.delete(DELETE_GOOD_URL, params={"idx": int(idx)}).json()
            dispatcher.utter_message(text=f"{name['name']} has been deleted!!")
        except Exception as _:
            dispatcher.utter_message(text="Cannot delete good. It does not exist.")


class ActionCanBeDeleted(Action):
    def name(self) -> str:
        return "action_can_be_deleted"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[str, Any]
    ) -> List[Dict[Text, Any]]:
        email = tracker.get_slot("add_user_email_login")
        if email:
            idx = tracker.get_slot("which_good_to_show")
            if idx:
                if idx.isdigit():
                    return [SlotSet("can_be_deleted", True)]
                else:
                    dispatcher.utter_message(
                        text="Please enter order of good you want to delete."
                    )
                    return [SlotSet("can_be_deleted", False)]
            else:
                dispatcher.utter_message(
                    text="Error: Select a good using list goods -> select :order:"
                )
                return [SlotSet("can_be_deleted", False)]

        else:
            dispatcher.utter_message(
                text="You are not logged in to perform the action."
            )
            return [SlotSet("can_be_deleted", False)]
