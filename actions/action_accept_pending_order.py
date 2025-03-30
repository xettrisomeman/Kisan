from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

import httpx
from config import ACCEPT_PENDING_ORDER


class ActionAcceptPendingOrder(Action):
    def name(self) -> str:
        return "action_accept_pending_order"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[str, Any]
    ) -> List[Dict[Text, Any]]:
        order_id = tracker.get_slot("which_good_to_accept")
        if order_id.isdigit():
            buyer_email = tracker.get_slot("add_user_email_login")
            res = httpx.put(
                ACCEPT_PENDING_ORDER.format(order_item_id=int(order_id)),
                params={"buyer_email": buyer_email},
            )
            if res.status_code == 200:
                res = res.json()
                dispatcher.utter_message(text=f"{res['name']} order has been accepted.")
            else:
                dispatcher.utter_message(text=f"Order with id:{order_id} not found.")
        else:
            dispatcher.utter_message(text="Please provide a valid order ID.")
