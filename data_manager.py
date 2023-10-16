import requests

HEADER = {"Authorization": "Bearer SHEETY API HERE"}
URL = "SHEETY LINK HERE"

class DataManager:
    #This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.destination_data = {}
        self.customer_data = {}
    def get_data(self):
        data = requests.get(url=f"{URL}/prices", headers=HEADER)
        self.destination_data = data.json()["prices"]
        return self.destination_data

    def get_customerinfo(self):
        data = requests.get(url=f"{URL}/users", headers=HEADER)
        self.customer_data = data.json()["users"]
        return self.customer_data

    def update_iata(self):
        for city in self.destination_data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            iata = requests.put(url=f"{URL}/prices/{city['id']}", json=new_data, headers=HEADER)
            print(iata.text)

    def update(self, key, value, id):
        new_val = {
            "price": {
                f"{key}": value
            }
        }
        response = requests.put(url=f"{URL}/prices/{id}", json=new_val, headers=HEADER)
        print(response.text)

