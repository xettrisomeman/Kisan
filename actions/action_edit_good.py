from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher


import httpx
from config import EDIT_GOOD_URL, DETAIL_GOOD_URL


class ActionEditGood(Action):
    def name(self) -> str:
        return "action_edit_good"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[str, Any]
    ) -> List[Dict[Text, Any]]:
        idx = tracker.get_slot("which_good_to_show").replace("good_detail_", "").strip()
        goods = httpx.get(DETAIL_GOOD_URL.format(id=int(idx))).json()
        new_price = (
            tracker.get_slot("new_price")
            if tracker.get_slot("new_price")
            else goods["price"]
        )
        new_quantity = (
            tracker.get_slot("change_quantity")
            if tracker.get_slot("change_quantity")
            else goods["quantity"]
        )
        email = tracker.get_slot("add_user_email_login")
        goods_new = {"price": float(new_price), "quantity": float(new_quantity)}
        res = httpx.put(
            EDIT_GOOD_URL, json=goods_new, params={"idx": int(idx), "email": email}
        )
        if res.status_code == 200:
            return [SlotSet("good_updated", "true")]
        else:
            return [SlotSet("good_updated", "false")]


class ActionCanBeEdited(Action):
    def name(self) -> str:
        return "action_can_be_edited"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[str, Any]
    ) -> List[Dict[Text, Any]]:
        email = tracker.get_slot("add_user_email_login")
        if email:
            idx = tracker.get_slot("which_good_to_show")
            if idx:
                if idx.isdigit():
                    res_detail = httpx.get(DETAIL_GOOD_URL.format(id=int(idx)))
                    if res_detail.status_code == 200:
                        res_detail = res_detail.json()
                        if res_detail["farmer"]["email"] == email:
                            return [SlotSet("can_be_edited", True)]
                        else:
                            dispatcher.utter_message(
                                text="You cannot edit the good you have not added"
                            )
                            return [SlotSet("can_be_edited", False)]
                    else:
                        dispatcher.utter_message(
                            text="Can't edit the good. Please try again."
                        )
                        return [SlotSet("can_be_edited", False)]
                else:
                    dispatcher.utter_message(
                        text="Please enter order of good you want to edit."
                    )
                    return [SlotSet("can_be_edited", False)]
            else:
                dispatcher.utter_message(
                    text="Error: Select a good using list goods -> select :order:"
                )
                return [SlotSet("can_be_edited", False)]

        else:
            dispatcher.utter_message(
                text="You are not logged in to perform the action."
            )
            return [SlotSet("can_be_edited", False)]
