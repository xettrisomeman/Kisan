from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

from config import LIST_GOOD_URL
import httpx


class ActionShowListGoods(Action):
    def name(self) -> str:
        return "action_show_list_goods"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[str, Any]
    ) -> List[Dict[Text, Any]]:
        try:
            res = httpx.get(LIST_GOOD_URL)
            if res.status_code == 200:
                goods = res.json()
                msg = ""
                for idx, good in enumerate(goods, start=1):
                    msg += f"{idx}.{good['name']} by {good['farmer']['email']}\n"
                dispatcher.utter_message(text=msg)
                return [SlotSet("is_good", True)]
            else:
                dispatcher.utter_message(
                    text="There are no goods available at the moment. Please add goods."
                )
                return [SlotSet("is_good", False)]

        except Exception as _:
            dispatcher.utter_message(
                text="Sorry, there was an error fetching the goods."
            )
