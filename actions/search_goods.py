from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from config import LIST_GOOD_URL, SEARCH_GOOD_URL
import httpx


class SearchGoods(Action):
    def name(self) -> str:
        return "search_goods"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[str, Any]
    ) -> List[Dict[Text, Any]]:
        query = tracker.get_slot("search_query")
        search = httpx.get(SEARCH_GOOD_URL, params={"query": query})
        dispatcher.utter_message(text=f"{search.json()}")
