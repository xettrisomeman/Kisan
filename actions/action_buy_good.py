from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher


import httpx
from config import BUY_GOODS_URL, DETAIL_GOOD_URL


class ActionBuyGood(Action):
    def name(self) -> str:
        return "action_buy_good"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[str, Any]
    ) -> List[Dict[Text, Any]]:
        quantity = tracker.get_slot("quantity_to_buy")
        idx = tracker.get_slot("which_good_to_show")
        current_user = tracker.get_slot("add_user_email_login")
        res_detail = httpx.get(DETAIL_GOOD_URL.format(id=int(idx))).json()
        seller_email = res_detail["farmer"]["email"]

        try:
            res_buy = httpx.post(
                BUY_GOODS_URL,
                json={
                    "buyer_email": current_user,
                    "seller_email": seller_email,
                    "idx": idx,
                    "quantity": quantity,
                },
            ).json()
            dispatcher.utter_message(
                text=f"You have succesfully bought {quantity} {res_detail['quantity_scale']} from {res_buy['name']}"
            )
        except Exception as e:
            dispatcher.utter_message(text=f"{e}")


class ActionCanBeBought(Action):
    def name(self) -> str:
        return "action_can_be_bought"

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
                            dispatcher.utter_message(
                                text="You cannot buy the good you have added"
                            )
                            return [SlotSet("can_be_bought", False)]
                        else:
                            return [SlotSet("can_be_bought", True)]
                    else:
                        dispatcher.utter_message(
                            text="Cannot find the good. Please try again."
                        )
                        [SlotSet("can_be_bought", False)]
                else:
                    dispatcher.utter_message(
                        text="Please enter order of good you want to buy."
                    )
                    [SlotSet("can_be_bought", False)]

            else:
                dispatcher.utter_message(
                    text="Error: Select a good using list goods -> select :order:"
                )
                [SlotSet("can_be_bought", False)]

        else:
            dispatcher.utter_message(
                text="You are not logged in to perform the action."
            )
            [SlotSet("can_be_bought", False)]
