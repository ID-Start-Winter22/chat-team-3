# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from sys import displayhook
from typing import Any, Text, Dict, List
from pyparsing import nestedExpr

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from . import mvg
import json

# NOTE(Michael): We could use this action to store the name in
#                the TrackerStore (in memory database) or a persitent DB
#                such as MySQL. But we need to store a key-value pair
#                to identify the user by id eg. (user_id, slotvalue)


class ActionStoreUserName(Action):

    def name(self) -> Text:
        return "action_store_name"

    def run(self, dispatcher, tracker, domain):
        username = tracker.get_slot("username")
        print("Sender ID: ", tracker.sender_id)

        return []


class ActionUserName(Action):

    def name(self) -> Text:
        return "action_get_name"

    def run(self, dispatcher, tracker, domain):
        username = tracker.get_slot("username")
        if not username:
            dispatcher.utter_message(" Du hast mir Deinen Namen nicht gesagt.")
        else:
            dispatcher.utter_message(' Du bist {}'.format(username))

        return []


class ActionMVG(Action):

    def name(self) -> Text:
        return "action_get_travel_time"

    def run(self, dispatcher, tracker, domain):
        from_station = tracker.get_slot("from_station")
        to_station = tracker.get_slot("to_station")
        if not from_station or not to_station:
            dispatcher.utter_message("Diese Stationen habe ich nicht erkannt!")
        else:
            result = json.loads(mvg.handle_route(from_station, to_station))
            print(result)
            if "error" in result:
                print("FEHLER!!!!!!!")
                dispatcher.utter_message(
                    "Sorry! Ich habe da mindestens eine Station nicht erkannt!")
            else:
                origin = result["from"]
                destination = result["to"]
                time_needed = result["time_needed"]
                dispatcher.utter_message("Du brauchst exakt: {} Minuten von {} nach {}. Gute Reise!".format(
                    time_needed, origin, destination))

        return []


class ActionYouTubeVideos(Action):
    def name(self) -> Text:
        return "action_send_youtube_video"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(
            "Hier sind ein paar Ubungen für dich. Viel Spaß im Training!")
        dispatcher.utter_message(attachment={
            "type": "video",
            "payload": {
                "titel": "Die besten Ubungen",
                "src": "https://www.youtube.com/embed/ii8WjM8Va70"
            }

        })
        return []


video_trainings = {"Po": ["https://www.youtube.com/embed/ii8WjM8Va70",
                          "https://www.youtube.com/embed/tn57ZkO8lnE",
                          "https://www.youtube.com/embed/VN8lB8ehpkk"],
                   "Bauch": ["https://www.youtube.com/embed/ouFOaLWmerk",
                             "https://www.youtube.com/embed/84EkBBwJc3A",
                             "https://www.youtube.com/embed/LbyGA5XrkF4"]
                   }


class ActionTrainingsVideos(Action):
    def name(self) -> Text:
        return "action_give_video0"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        muskelgruppe_detected = tracker.get_slot("muskelgruppe")
        if not muskelgruppe_detected:
            dispatcher.utter_message(
                "Sorry, aber ich habe die Muskelgruppe nicht erkannt. Probier es nochmal bitte 🤓")
        elif muskelgruppe_detected in video_trainings.keys():
            for key in video_trainings:
                if key == muskelgruppe_detected:
                    link = video_trainings[muskelgruppe_detected][0]
                    dispatcher.utter_message("Hier ist ein Videotraining für {}. Viel Spaß 💪🏻🔥".format(muskelgruppe_detected))
                    dispatcher.utter_message(attachment={
                        "type": "video",
                        "payload": {
                            "titel": "Die besten Ubungen",
                            "src": link
            }})
        return []
