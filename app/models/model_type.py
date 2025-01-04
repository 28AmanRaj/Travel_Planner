from typing import TypedDict
from pydantic import BaseModel


class TripPlanRequest(BaseModel):
    Destination: str
    Duration: int
    Number_of_People: int
    Traveling_With: str
    Interests: str
    Itinerary_Style: str
    Budget: str


class TripPlanState(TypedDict):
    Destination: str
    Duration: int
    Number_of_People: int
    Traveling_With: str
    Interests:str
    Itinerary_Style: str
    Budget: str
    Destination_Detail:str
    Recommended_Places:str
    Recommended_Activity:str
    Recommended_Hotels:dict
    Recommended_Links:dict
    Travel_Plan:str
    