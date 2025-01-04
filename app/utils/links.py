from langchain_community.utilities import GoogleSerperAPIWrapper
from dotenv import load_dotenv
from app.models import model_type as models

load_dotenv()

search = GoogleSerperAPIWrapper()

async def fetch_links(state: models.TripPlanState) ->dict:
    """ Fetches links from google for famaous plances in the destination """

    destination = state["Destination"]
    duration = state["Duration"]
    interests = state["Interests"]
    traveling_with = state["Traveling_With"]

    query = f"travel guide for {destination} for {duration} days, my interests are {interests} and I am traveling with {traveling_with}"


    try:
        search_results = search.results(query)  
        organic_results = search_results.get("organic", [])
        
        top_links = []  

        
        for entry in organic_results[:5]: 
            url = entry.get("link", "")
            if url: 
                top_links.append(url)

       
        if not top_links:
            top_links = ["No relevant links found."]
        
        return {"links": top_links}

    except Exception as e:
        return {"error": str(e)}


