from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from app.models import model_type as model
import logging
from app.utils.prompt import generate_destination_detail_prompt, place_recommendation_prompt, activity_recommendation_prompt, travel_plan_assembly_prompt, travel_plan_assembly_user_prompt
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
    system_message = SystemMessage(
        content=(place_recommendation_prompt)
    )

    messages = [system_message, HumanMessage(state["Destination"])]
    response = llm.generate([messages])

    place_recommendation = response.generations[0][0].text.strip()
    logger.info(f"Generated place recommendation: place{place_recommendation}")
    state["Place_Recommendation"] = place_recommendation
    return place_recommendation

async def activity_recommendation(state: model.TripPlanState):
    """Generates activity recommendation."""
    system_message = SystemMessage(
        content=(activity_recommendation_prompt)
    )

    messages = [system_message, HumanMessage(state["Destination"])]
    response = llm.generate([messages])

    activity_recommendation = response.generations[0][0].text.strip()
    logger.info(f"Generated activity recommendation: {activity_recommendation}")
    state["Activity_Recommendation"] = activity_recommendation
    return  activity_recommendation

async def travel_plan_assembly(state: model.TripPlanState):
    """Assembles travel plan."""
    destination_detail = state["Destination_Detail"]
    places = state["Place_Recommendation"]
    activity = state["Activity_Recommendation"]
    itinerary_style = state["Itinerary_Style"]
    duration = state["Duration"]
    



    user_prompt = travel_plan_assembly_user_prompt.format(destination_detail=destination_detail, places=places, activity=activity, itinerary_style=itinerary_style, Duration=duration)
    system_message = SystemMessage(
        content=(travel_plan_assembly_prompt)
    )
    messages = [system_message, HumanMessage(user_prompt)]
    
    
    response =llm.generate([messages])
    travel_plan = response.generations[0][0].text.strip()
    logger.info(f"Assembled travel plan: {travel_plan}")
    return travel_plan
    