from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

import httpx
from config import ADD_GOOD_URL


class AddGood(Action):
    def name(self) -> str:
        return "add_good"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[str, Any]
    ) -> List[Dict[Text, Any]]:
        email = tracker.get_slot("add_user_email_login")
        name = tracker.get_slot("add_good_name")
        description = tracker.get_slot("add_good_description")
        price = tracker.get_slot("add_good_price")
        quantity = tracker.get_slot("add_good_quantity")
        quantity_scale = tracker.get_slot("add_good_quantity_scale")

        payload = {
            "name": name,
            "description": description,
            "price": price,
            "quantity": quantity,
            "quantity_scale": quantity_scale,
        }
        response = httpx.post(ADD_GOOD_URL, json=payload, params={"email": email})
        if response.status_code == 201:
            return [SlotSet("return_value", "added")]
        else:
            return [SlotSet("return_value", "failed")]
