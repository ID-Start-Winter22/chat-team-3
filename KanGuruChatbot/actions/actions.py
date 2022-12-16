# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"
import random
from sys import displayhook
from typing import Any, Text, Dict, List
from pyparsing import nestedExpr

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

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


video_trainings = {"Po": ["https://www.youtube.com/embed/bggX6ocjojk",
                          "https://www.youtube.com/embed/tn57ZkO8lnE",
                          "https://www.youtube.com/embed/VN8lB8ehpkk"],
                   "Bauch": ["https://www.youtube.com/embed/ouFOaLWmerk",
                             "https://www.youtube.com/embed/84EkBBwJc3A",
                             "https://www.youtube.com/embed/LbyGA5XrkF4"],
                   "Beine": ["https://www.youtube.com/embed/b9DFYywGneA",
                             "https://www.youtube.com/embed/bcH-qcnpy20",
                             "https://www.youtube.com/embed/_wt_N-FXcZ0"],
                   "Nacken": ["https://www.youtube.com/embed/ii8WjM8Va70",
                              "https://www.youtube.com/embed/ea86IuyeiNM",
                              "https://www.youtube.com/embed/xWJJElttl4E"],
                   "Schultern": ["https://www.youtube.com/embed/OMpGZclL24M",
                                 "https://www.youtube.com/embed/7_0suCmMbfg",
                                 "https://www.youtube.com/embed/qQduXPnxcBA"],
                   "Stretching": ["https://www.youtube.com/embed/qFgwrTc1e1I",
                                  "https://www.youtube.com/embed/qULTwquOuT4",
                                  "https://www.youtube.com/embed/g_tea8ZNk5A"],
                   "Trizeps": ["https://www.youtube.com/embed/elXOc-4yvNI",
                               "https://www.youtube.com/embed/BiKj6GSDxAs",
                               "https://www.youtube.com/embed/NmUMcKKuZSE"],
                   "Bizeps": ["https://www.youtube.com/embed/sMW2HRaCz3A",
                              "https://www.youtube.com/embed/Ja5qlQH3Plg",
                              "https://www.youtube.com/embed/-pT0t2ScJ00"],
                   "Brust": ["https://www.youtube.com/embed/VEkA5wDsPUk",
                             "https://www.youtube.com/embed/mLhtgu_CQDY",
                             "https://www.youtube.com/embed/MwprhUnF4PA"],
                   "Rücken": ["https://www.youtube.com/embed/8CdTc8nXzrA",
                              "https://www.youtube.com/embed/f1dtA3saKk0",
                              "https://www.youtube.com/embed/wNXBsazLt9Y"],
                   "Arme": ["https://www.youtube.com/embed/JfFV-mll0xU",
                            "https://www.youtube.com/embed/ZNQC_Dzr10U",
                            "https://www.youtube.com/embed/Z2DrCQOalBs"],
                   "Waden": ["https://www.youtube.com/embed/Ox4N6MkvLV8",
                             "https://www.youtube.com/embed/xZvbvB5MPWA",
                             "https://www.youtube.com/embed/fx3eTJ_D95M"],
                   "Handgelenke": ["https://www.youtube.com/embed/KEY9D-PDWXc",
                                   "https://www.youtube.com/embed/XZ-0BRG1OiM",
                                   "https://www.youtube.com/embed/1BO8Sgx0pBY"],
                   "Kardiotraining": ["https://www.youtube.com/embed/O9jWAf98-rU",
                                      "https://www.youtube.com/embed/ympgQ2GWWcY",
                                      "https://www.youtube.com/embed/BMAvdnzuF9E"],
                   "Aufwärmen": ["https://www.youtube.com/embed/kic4EeXOfNw",
                                 "https://www.youtube.com/embed/rVXMObcJTK8",
                                 "https://www.youtube.com/embed/p-v_obY-lYw"],
                   "Yoga": ["https://www.youtube.com/embed/g_tea8ZNk5A",
                                 "https://www.youtube.com/embed/oX6I6vs1EFs",
                                 "https://www.youtube.com/embed/7ciS93shMNQ"]
                   }

video_for_you = ["Hier ist ein Videotraining für {}.", "Hier ist ein Workout für {}.",
                 "Hier ist ein cooles Video, um {} zu trainieren!", "Hier findest Du gute Übungen für {}.",
                 "Das Video bringt deine {}muskeln richtig in Form.", "Hier sind die besten Übungen für {}.",
                 "Hier ist ein Video für {}.", "Hier sind ein paar Übungen für {}.",
                 "Hier ein Workout für {}. Die 10 Minuten schaffst du!", "Hier einige Übungen für {}.",
                 "10 Minuten. Volle Power. Die Zeit hast du!", "Mit dem Video kannst du {} gut trainieren!",
                 "Hier ein Video. Aufgeben ist keine Option!", "Hier findest du ein Workout für {}. No pain, no gain!",
                 "Mit diesen Übungen kriegst du starke {}muskeln!", "Hier ein tolles Workout für {}.",
                 "Die besten Übungen für {} findest du hier!", "Wenn du deine {}muskeln verstärken willst, komm an diesem Workout nicht vorbei!",
                 "Hier ein tolles {}-Workout für dich!", "Hier einige Übungen für deine {}muskeln.", "Diese Übungen sind perfekt für starke {}.",
                 "Starke {}muskeln sind wichtig! Los geht's!", "Hier ein paar einfache Übungen! Das schaffst du!", "Hier ist ein {}-Workout für dich! 🙌🏼",
                 "Gute Wahl 👍🏻 {}muskeln sind sehr wichtig für deinen Körper! 😇", "Ich habe ein Video für dich 🤓🏋🏽"]

video_cardio_for_you = ["Hier ist ein Kardiotraining für dich 🤩",
                        "Viel Spaß beim Verbessern deiner Ausdauer! 🏃🏻‍♀️", "Kardio ist wichtig. Hier mein erster Vorschlag! 🏃🏻"]
video_stretching_for_you = ["Hier ist ein Stretching-Workout für dich! 🥰",
                            "Hier ist ein Video für dich, entspann dich gut 🙏🏻", "Hier ist mein erster Vorschlag. Verbessere deine Flexibilität! 🧘🏻"]
video_yoga_for_you = ["Hier ist ein Yoga-Training für dich 🧘🏻‍♀️",
                      "Hier ist mein erster Vorschlag 🧘🏻‍♀️", "Hier ist ein Video. Nimm dir Zeit für eine Entspannung! 🙏🏻"]
video_aufwaermen_for_you = ["Wärme dich gut auf! 🤸🏻", "Hier habe ich ein tolles Warm Up für dich! 🏋🏽🔥",
                            "Nach diesen Aufwärmübungen bist du bereit für dein Workout! 🚀"]

have_nice_training = ["Viel Spaß im Training! 🤟🏻🤩", "Viel Kraft im Training! 🔥💪🏻", "Genieß das Training!", "Viel Erfolg! 👏🏻🤩",
                      "Viel Erfolg im Training!", "Viel Spaß bei deinem Workout!", "Ich wünsch dir ein erfolgreiches Workout! 😎✊🏻",
                      "Viel Spaß beim Trainieren! Gib alles! 🔥", "Los geht's! Hab ein tolles Workout! 🏋🏽💪🏻",
                      "Zeit für's Training! Viel Spaß! 👊", "Your only limit is your mind, los geht's! 🚀",
                      "Wenn Du alles gibst, kannst Du Dir nichts vorwerfen! 🔥💪🏻", "Viel Spaß mit den Übungen! 🏋🏽🔥",
                      "Los geht's Sportler! No excuses! 🚀💪🏻", "Zeit, aktiv zu werden. Los geht's! 😎✊🏻", "Du schaffst das! 💪🏻🔥"]

one_more_video = ["Kein Problem. Hier ist noch ein Video für dich!", "Hier hab ich ein anderes Video für dich!",
                  "Das wäre ein alternatives Video!", "Kein Problem, dieses Video hätte ich auch noch!"]
last_video = ["Mein letzter Vorschlag 😏💪🏻", "Das Beste kommt zum Schluss 🏋🏽🔥",
              "Ein Voschlag habe ich noch fûr dich 🏋🏻‍♀️💪🏻", "Alle guten Dinge sind drei ✌🏻😎"]


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
                    if muskelgruppe_detected == "Stretching":
                        dispatcher.utter_message(
                            (random.choice(video_stretching_for_you)))
                    elif muskelgruppe_detected == "Kardiotraining":
                        dispatcher.utter_message(
                            (random.choice(video_cardio_for_you)))
                    elif muskelgruppe_detected == "Yoga":
                        dispatcher.utter_message(
                            (random.choice(video_yoga_for_you)))
                    elif muskelgruppe_detected == "Aufwärmen":
                        dispatcher.utter_message(
                            (random.choice(video_aufwaermen_for_you)))
                    else:
                        dispatcher.utter_message(
                            (random.choice(video_for_you)).format(muskelgruppe_detected))
                    dispatcher.utter_message(
                        attachment={"type": "video", "payload": {"src": link}})
                    dispatcher.utter_message(random.choice(have_nice_training))
        return []


class ActionTrainingsVideos1(Action):
    def name(self) -> Text:
        return "action_give_video1"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        muskelgruppe_detected = tracker.get_slot("muskelgruppe")
        if not muskelgruppe_detected:
            dispatcher.utter_message(
                "Sorry, aber ich habe die Muskelgruppe nicht erkannt. Probier es nochmal bitte 🤓")
        elif muskelgruppe_detected in video_trainings.keys():
            for key in video_trainings:
                if key == muskelgruppe_detected:
                    link = video_trainings[muskelgruppe_detected][1]
                    dispatcher.utter_message(random.choice(one_more_video))
                    dispatcher.utter_message(
                        attachment={"type": "video", "payload": {"src": link}})
                    dispatcher.utter_message(random.choice(have_nice_training))
        return []


class ActionTrainingsVideos2(Action):
    def name(self) -> Text:
        return "action_give_video2"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        muskelgruppe_detected = tracker.get_slot("muskelgruppe")
        if not muskelgruppe_detected:
            dispatcher.utter_message(
                "Sorry, aber ich habe die Muskelgruppe nicht erkannt. Probier es nochmal bitte 🤓")
        elif muskelgruppe_detected in video_trainings.keys():
            for key in video_trainings:
                if key == muskelgruppe_detected:
                    link = video_trainings[muskelgruppe_detected][2]
                    dispatcher.utter_message(random.choice(last_video))
                    dispatcher.utter_message(
                        attachment={"type": "video", "payload": {"src": link}})
                    dispatcher.utter_message(random.choice(have_nice_training))
        return []
