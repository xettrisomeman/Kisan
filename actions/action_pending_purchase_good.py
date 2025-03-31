from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher


import httpx
from config import BUY_PENDING_HISTORY


class ShowPendingPurchaseGood(Action):
    def name(self) -> str:
        return "show_pending_purchase_good"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[str, Any]
    ) -> List[Dict[Text, Any]]:
        logged_in = tracker.get_slot("logged_in")
        if logged_in:
            email = tracker.get_slot("add_user_email_login")
            responses = httpx.get(
                BUY_PENDING_HISTORY, params={"buyer_email": email}
            ).json()
            if responses:
                for idx, res in enumerate(responses[:5], start=1):
                    res_msg = (
                        f"ID: {idx}\n"
                        f"Name: {res['name']}\n"
                        f"Quantity: {res['quantity']} Price: {res['price']} Subtotal: {res['subtotal']}\n"
                        f"Status: {res['status']}"
                    )
                    dispatcher.utter_message(text=res_msg)
                    return [SlotSet("is_pending", True)]
            else:
                dispatcher.utter_message(text="You have no purchases in pending.")
                return [SlotSet("is_pending", False)]
        else:
            dispatcher.utter_message(
                text="You have to be logged in to perform the action."
            )
