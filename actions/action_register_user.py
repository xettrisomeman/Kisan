from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

from config import REGISTER_USER_URL
import httpx

from email_validator import validate_email, EmailNotValidError


class RegisterUser(Action):
    def name(self) -> str:
        return "register_user"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[str, Any]
    ) -> List[Dict[Text, Any]]:
        name = tracker.get_slot("add_user_name")
        email = tracker.get_slot("add_user_email")
        location = tracker.get_slot("add_user_location")
        interests = tracker.get_slot("add_user_interests")
        password = tracker.get_slot("add_user_password")

        payload = {
            "name": name,
            "email": email,
            "location": location,
            "password": password,
            "interests": interests,
        }
        response = httpx.post(REGISTER_USER_URL, json=payload)
        if response.status_code == 200:
            return [SlotSet("return_value", "success")]
        else:
            return [SlotSet("return_value", "failure")]


class ValidateTwoPassword(Action):
    def name(self) -> str:
        return "validate_two_password"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[str, Any]
    ) -> List[Dict[Text, Any]]:
        password1 = tracker.get_slot("add_user_password")
        password2 = tracker.get_slot("add_user_password_confirmation")
        if password1 != password2:
            return [SlotSet("pw_validated", False)]
        return [SlotSet("pw_validated", True)]


class ValidatePasswordLength(Action):
    def name(self) -> str:
        return "validate_password_length"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[str, Any]
    ) -> List[Dict[Text, Any]]:
        password1 = tracker.get_slot("add_user_password")
        if len(password1) < 8:
            return [SlotSet("pw_validated_length", False)]
        return [SlotSet("pw_validated_length", True)]


class ValidateEmail(Action):
    def name(self) -> str:
        return "validate_email"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[str, Any]
    ) -> List[Dict[Text, Any]]:
        email = tracker.get_slot("add_user_email")
        try:
            _ = validate_email(email, check_deliverability=False)
            return [SlotSet("valid_email", True)]
        except EmailNotValidError as _:
            return [SlotSet("valid_email", False)]
