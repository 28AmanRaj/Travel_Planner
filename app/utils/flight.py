from serpapi import GoogleSearch
import os
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


load_dotenv()

serpapi_key = os.getenv("SERPAPI_KEY")

async def get_flight_details(departure_id, arrival_id, date):
    logging.info(f"Fetching flights from {departure_id} to {arrival_id} on {date}...")
    params = {
        "engine": "google_flights",
        "departure_id": departure_id,
        "arrival_id": arrival_id,
        "type":"2",
        "outbound_date": date,
        "sort_by":"2",
        "currency": "INR",
        "hl": "en",
        "api_key": serpapi_key  # Replace with your actual SerpAPI key
    }

    try:
        search = GoogleSearch(params)
        results = search.get_dict()
        
        flights_data = results.get("other_flights", [])  # Adjust this key if needed

        if not isinstance(flights_data, list) or not flights_data:
            logging.warning("No flights found matching the criteria.")
            return {"error": "No flights found matching the criteria."} 

        filtered_flights = []
        for flight in flights_data[:3]:
            flight_info = flight["flights"][0]  # First flight segment
            booking_token = flight.get("booking_token", "")
            params_links = {
                "engine": "google_flights",
                "departure_id": departure_id,
                "arrival_id": arrival_id,
                "type":"2",
                "outbound_date": date,
                "currency": "INR",
                "hl": "en",
                "booking_token": booking_token,
                "api_key": serpapi_key
                }

            # Construct Google Flights booking URL
            # booking_url = f"https://www.google.com/flights?hl=en#flt={booking_token}" if booking_token else "Booking link not available"
            search_links = GoogleSearch(params_links)
            booking_url = search_links.get_dict().get("search_metadata", {}).get("google_flights_url", "")

            flight_details = {
                "Departure Airport": flight_info["departure_airport"]["name"],
                "Departure Time": flight_info["departure_airport"]["time"],
                "Arrival Airport": flight_info["arrival_airport"]["name"],
                "Arrival Time": flight_info["arrival_airport"]["time"],
                "Duration (min)": flight_info["duration"],
                "Airline": flight_info["airline"],
                "Airplane": flight_info["airplane"],
                "Flight Number": flight_info["flight_number"],
                "Price (INR)": flight["price"],
                "Type": flight["type"],
                "Booking Link": booking_url
            }
            filtered_flights.append(flight_details)

        logging.info(f"Successfully fetched {len(filtered_flights)} flights.")
        return {"flights": filtered_flights}

    except Exception as e:
        logging.error(f"Error fetching flight details: {e}")
        return {"error": "An error occurred while fetching flight details."}
