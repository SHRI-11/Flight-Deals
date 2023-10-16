import requests
from flight_data import FlightData

API = {"apikey": "YOUR API KEY"}
ENDPOINT = "https://api.tequila.kiwi.com"

class FlightSearch:
    #This class is responsible for talking to the Flight Search API.
    def get_destination_code(self, city_name):
        params = {
            "term": city_name,
            "location_types": "city"
        }
        response = requests.get(url=f"{ENDPOINT}/locations/query", params=params, headers=API)
        code = response.json()["locations"][0]["code"]
        return code

    def get_flight_price(self, from_city_code, to_city_code, from_date, to_date, stop_overs=0):
        params = {
            "fly_from": from_city_code,
            "fly_to": to_city_code,
            "date_from": from_date.strftime("%d/%m/%Y"),
            "date_to": to_date.strftime("%d/%m/%Y"),
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "flight_type": "round",
            "one_for_city": 1,
            "max_stopovers": stop_overs,
            "curr": "GBP"
        }
        response = requests.get(url=f"{ENDPOINT}/v2/search", params=params, headers=API)
        try:
            data = response.json()["data"][0]
        except IndexError:
            return None
        if stop_overs != 0:
            flight_data = FlightData(
                price=data["price"],
                origin_city=data["route"][0]["cityFrom"],
                origin_airport=data["route"][0]["flyFrom"],
                destination_city=data["route"][1]["cityTo"],
                destination_airport=data["route"][1]["flyTo"],
                out_date=data["route"][0]["local_departure"].split("T")[0],
                return_date=data["route"][3]["local_departure"].split("T")[0],
                stop_overs=1,
                via_city=data["route"][1]["cityFrom"]
            )
            return flight_data
        else:
            flight_data = FlightData(
                price=data["price"],
                origin_city=data["route"][0]["cityFrom"],
                origin_airport=data["route"][0]["flyFrom"],
                destination_city=data["route"][0]["cityTo"],
                destination_airport=data["route"][0]["flyTo"],
                out_date=data["route"][0]["local_departure"].split("T")[0],
                return_date=data["route"][1]["local_departure"].split("T")[0],
            )
            return flight_data
