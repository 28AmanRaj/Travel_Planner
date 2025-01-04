from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from app.models import model_type as model
import logging
from app.utils.prompt import generate_destination_detail_prompt, place_recommendation_prompt, activity_recommendation_prompt, travel_plan_assembly_prompt, travel_plan_assembly_user_prompt, place_recommendation_user_prompt, activity_recommendation_user_prompt
from dotenv import load_dotenv
import os


load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

llm = ChatOpenAI(model="gpt-4o", temperature=0.7)

async def generate_destination_detail(state: model.TripPlanState):
    """Generates destination detail."""
    system_message = SystemMessage(
        content=(generate_destination_detail_prompt)
    )

    messages = [system_message, HumanMessage(state["Destination"])]
    response = llm.generate([messages])

    detail = response.generations[0][0].text.strip()
    logger.info(f"Generated destination detail: {detail}")
    state["Destination_Detail"] = detail
    return detail

async def place_recommendation(state: model.TripPlanState):
    """Generates place recommendation."""
    destination = state["Destination"]
    duration = state["Duration"]
    interests = state["Interests"]
    travelin_with = state["Traveling_With"]

    user_promt = place_recommendation_user_prompt.format(Destination=destination, Duration=duration, Interests=interests, Traveling_With=travelin_with)
    system_message = SystemMessage(
        content=(place_recommendation_prompt)
    )

    messages = [system_message, HumanMessage(user_promt)]
    response = llm.generate([messages])

    place_recommendation = response.generations[0][0].text.strip()
    logger.info(f"Generated place recommendation: place{place_recommendation}")
    state["Recommended_Places"] = place_recommendation
    return place_recommendation

async def activity_recommendation(state: model.TripPlanState):
    """Generates activity recommendation."""
    duration = state["Duration"]
    destination = state["Destination"]
    places = state["Recommended_Places"]
    interests = state["Interests"]

    user_prompt = activity_recommendation_user_prompt.format(Destination=destination, Duration=duration, Places=places, Interests=interests)
    system_message = SystemMessage(
        content=(activity_recommendation_prompt)
    )

    messages = [system_message, HumanMessage(user_prompt)]
    response = llm.generate([messages])

    activity_recommendation = response.generations[0][0].text.strip()
    logger.info(f"Generated activity recommendation: {activity_recommendation}")
    state["Recommended_Activity"] = activity_recommendation
    return  activity_recommendation

async def travel_plan_assembly(state: model.TripPlanState):
    """Assembles travel plan."""
    destination_detail = state["Destination_Detail"]
    places = state["Recommended_Places"]
    activity = state["Recommended_Activity"]
    itinerary_style = state["Itinerary_Style"]
    duration = state["Duration"]
    hotel_links = state["Recommended_Hotels"]
    recommended_link = state["Recommended_Links"]
    



    user_prompt = travel_plan_assembly_user_prompt.format(destination_detail=destination_detail, places=places, activity=activity, itinerary_style=itinerary_style, duration=duration, hotel_links=hotel_links, recommended_link=recommended_link)
    system_message = SystemMessage(
        content=(travel_plan_assembly_prompt)
    )
    messages = [system_message, HumanMessage(user_prompt)]
    
    
    response =llm.generate([messages])
    travel_plan = response.generations[0][0].text.strip()
    logger.info(f"Assembled travel plan: {travel_plan}")
    return travel_plan

