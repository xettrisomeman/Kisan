from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

import httpx
from config import CANCEL_PENDING_ORDER


class ActionCancelPendingOrder(Action):
    def name(self) -> str:
        return "action_cancel_pending_order"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[str, Any]
    ) -> List[Dict[Text, Any]]:
        order_id = tracker.get_slot("which_good_to_cancel")
        if order_id.isdigit():
            email = tracker.get_slot("add_user_email_login")
            res = httpx.delete(
                CANCEL_PENDING_ORDER.format(id=int(order_id)), params={"email": email}
            )
            if res.status_code == 200:
                res = res.json()
                dispatcher.utter_message(
                    text=f"{res['name']} order has been cancelled."
                )
            else:
                dispatcher.utter_message(text=f"Goods with id:{order_id} not found.")
        else:
            dispatcher.utter_message(text="Please write ordername.")
