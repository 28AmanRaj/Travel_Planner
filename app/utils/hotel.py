from langchain_community.utilities import GoogleSerperAPIWrapper
from dotenv import load_dotenv
from app.models import model_type as models


load_dotenv()


search = GoogleSerperAPIWrapper()


async def fetch_hotels(state: models.TripPlanState) -> dict:
    """
    Fetches the top highly-rated hotel recommendation near a specified location based on budget.

    Args:
        location (str): The name of the location to search hotels near.
        budget (str): The budget category ("budget", "mid-range", or "expensive").

    Returns:
        dict: A dictionary with the hotel's name, snippet, and link.
    """
 
    
    locations = extract_locations(state["Recommended_Places"])
    destination = state["Destination"]

    all_hotels = {}

    for location in locations:
        query = f"site:tripadvisor.com highly rated {state['Budget']} hotels near {location},{destination}"

        try:
           
            results = search.results(query)
            
           
            organic_results = results.get("organic", [])
            
            if organic_results:
               
                first_entry = organic_results[0]
                url = first_entry.get("link", "")
                title = first_entry.get("title", "")
                snippet = first_entry.get("snippet", "")
                
                if "tripadvisor.com" in url: 
                    all_hotels[location] = {
                        "title": title,
                        "link": url,
                        "snippet": snippet
                    }
            else:
               
                all_hotels[location] = {
                    "title": "No results found",
                    "link": "",
                    "snippet": "No hotel found matching the criteria."
                }

        except Exception as e:
           
            all_hotels[location] = {
                "title": "Error fetching data",
                "link": "",
                "snippet": str(e)
            }

    return all_hotels


def extract_locations(locations_text):
    """
    Extracts individual locations from a multi-day itinerary text, excluding day markers.

    Args:
        locations_text (str): The itinerary text containing locations.

    Returns:
        list: A list of locations.
    """
   
    lines = locations_text.split("\n")
    locations = []

    for line in lines:
        
        if "Day" not in line and line.strip():
            locations.append(line.strip())
    
    return locations


