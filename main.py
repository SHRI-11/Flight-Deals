from data_manager import DataManager
from datetime import datetime, timedelta
from flight_search import FlightSearch
from notification_manager import NotificationManager

FROM_CITY_IATA = "LON"

flightsearch = FlightSearch()
datamanager = DataManager()
notificationmanager = NotificationManager()

sheet_data = datamanager.get_data()
customer_data = datamanager.get_customerinfo()

if sheet_data[0]["iataCode"] == "":
    for destination in sheet_data:
        destination["iataCode"] = flightsearch.get_destination_code(destination["city"])
    datamanager.destination_data = sheet_data
    datamanager.update_iata()

tom = datetime.now() + timedelta(days=1)
mon6 = datetime.now() + timedelta(days=6*30)

for destination in sheet_data:
    flight = flightsearch.get_flight_price(FROM_CITY_IATA, destination['iataCode'], tom, mon6)
    stopovers = 0
    if flight is None:
        stopovers = 2
        flight = flightsearch.get_flight_price(FROM_CITY_IATA, destination['iataCode'], tom, mon6, stopovers)
    if destination["lowestPrice"] > flight.price:
        destination["lowestPrice"] = flight.price
        datamanager.update("lowestPrice", destination["lowestPrice"], destination["id"])
        for row in customer_data:
            user = row["email"]
            notificationmanager.send_email(flight.price, flight.origin_city, flight.origin_airport,
                                           flight.destination_city, flight.destination_airport,
                                           flight.out_date, flight.return_date, user, stopovers, flight.via_city)
