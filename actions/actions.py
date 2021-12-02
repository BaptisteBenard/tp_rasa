# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests

dict_weather = {"sn": "It's snowy.",
        "sl": "It sleets.",
        "h": "It hails.",
        "t": "There is thunder.",
        "hr": "There is heavy rain.",
        "lr": "It is a bit rainy.",
        "s": "There are showers.",
        "hc": "There are heavy clouds.",
        "lc": "There are light clouds.",
        "c": "Weather is clear today."}

class ActionWeather(Action):

    def name(self) -> Text:
        return "action_weather"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:


        p = { "query": "bordeaux" }
        r = requests.get("https://www.metaweather.com//api/location/search/", params = p)
        j = r.json()[0]

        p = { }
        r = requests.get("https://www.metaweather.com//api/location/" + str(j["woeid"]) + "/", params = p)
        j = r.json()
        data = j["consolidated_weather"][0]
        abb, temp = data["weather_state_abbr"], data["the_temp"]
        w_ph = dict_weather[abb]
        temp_ph = " The temperature is " + str(round(temp)) + "°C."

        dispatcher.utter_message(text=w_ph + temp_ph)

        return []