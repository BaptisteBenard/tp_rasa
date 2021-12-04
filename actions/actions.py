# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import AllSlotsReset, FollowupAction
import requests
import random

dict_weather = {"sn": "It's snowy",
        "sl": "It sleets",
        "h": "It hails",
        "t": "There is thunder",
        "hr": "There is heavy rain",
        "lr": "It is a bit rainy",
        "s": "There are showers",
        "hc": "There are heavy clouds",
        "lc": "There are light clouds",
        "c": "Weather is clear today"}

answers_weather_not_found= ["I don't know this place, can you reformulate please ?",
        "I don't have data on this location, maybe try a more famous place",
        "I can't find any data, can you write a more important place please ?"]

class ActionWeather(Action):

    def name(self) -> Text:
        return "action_weather"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return ["place"]

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        place = str(tracker.get_slot("place"))
        place_l = place.lower()
        p = { "query": place_l }
        r = requests.get("https://www.metaweather.com//api/location/search/", params = p)
        j = r.json()

        if len(j) == 0:
            dispatcher.utter_message(text=random.choice(answers_weather_not_found))
            return [AllSlotsReset()]+[FollowupAction("weather_form")]

        j = j[0]
        p = { }
        r = requests.get("https://www.metaweather.com//api/location/" + str(j["woeid"]) + "/", params = p)
        j = r.json()
        data = j["consolidated_weather"][0]
        abb, temp = data["weather_state_abbr"], data["the_temp"]
        w_ph = dict_weather[abb] + ' in ' + place + "."
        temp_ph = " The temperature is " + str(round(temp)) + "°C."

        dispatcher.utter_message(text=w_ph + temp_ph)

        return [AllSlotsReset()]
