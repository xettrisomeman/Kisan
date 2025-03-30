from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

from config import DETAIL_GOOD_URL
import httpx
import re


class ActionGoodDetail(Action):
    def name(self) -> str:
        return "action_good_detail"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[str, Any]
    ) -> List[Dict[Text, Any]]:
        idx = tracker.get_slot("which_good_to_show").replace("good_detail_", "").strip()
        if idx:
            res = httpx.get(DETAIL_GOOD_URL.format(id=int(idx)))
            if res.status_code == 200:
                res = res.json()
                if res["price"] != res["previous_price"]:
                    differences = res["price"] - res["previous_price"]
                    if differences < 0:
                        price_change_percentage = (differences / res["price"]) * 100
                        price = f"Price: {res['price']} (Decreased by {price_change_percentage:.2f}%)"
                    else:
                        price_change_percentage = (differences / res["price"]) * 100
                        price = f"Price: {res['price']} (Increased by {price_change_percentage:.2f}%)"
                else:
                    price = f"Price: {res['price']}"

                messages = (
                    f"Name: {res['name']}\n"
                    f"Description: {res['description']}\n"
                    f"{price}\n"
                    f"Quantity: {res['quantity']} {res['quantity_scale']}\n"
                    f"Seller: {res['farmer']['name']}"
                )
                dispatcher.utter_message(messages)
            else:
                dispatcher.utter_message(text="Did not find any goods.")
        else:
            dispatcher.utter_message(text="Error selecting goods.")
