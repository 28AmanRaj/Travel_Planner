from typing import TypedDict
from pydantic import BaseModel
from typing import Optional




class TripPlanRequest(BaseModel):
    Destination: str
    Duration: int
    Number_of_People: int
    Traveling_With: str
    Interests: str
    Itinerary_Style: str
    Budget: str
    Departure_id: Optional[str] = None
    Arrival_id: Optional[str] = None
    Date: Optional[str] = None
    


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
    Recommended_flights:dict
    Recommended_dinning:dict
    Travel_Plan:list
    Departure_id: Optional[str]
    Arrival_id: Optional[str]
    Date: Optional[str]


from typing_extensions import Annotated



class AssembledTravelPlan(TypedDict):
    """
    Represents a fully assembled travel plan.
    """

    Destination_Overview: Annotated[
        str,
        ...,
        (
            "Destination Overview:\n"
            "\nThis section provides an introduction to the destination, "
            "highlighting key attractions, culture, and unique features.\n"
        )
    ]

    Day_by_Day_Plan: Annotated[
        str,
        ...,
        (
            "Day-by-Day Plan:\n"
            "\nThis section contains the detailed itinerary for each day of the trip.\n"
            "\nEach day is structured as follows:\n"
            "\n Morning:\n"
            "       - Activities planned for the morning session.\n"
            "\nAfternoon:\n"
            "       - Activities planned for the afternoon session.\n"
            "\nEvening:\n"
            "       - Activities planned for the evening session.\n"
            "\nDining Options:\n"
            "       - Recommended restaurants for dinning.\n"
            "\nHotels:\n"
            "       - Suggested accommodations near major attractions.\n"
        )
    ]

    Recommended_Links: Annotated[
        str,
        ...,
        (
            "Recommended Links:\n"
            "\nThis section includes useful travel guides, blog posts, and other references "
            "to help travelers plan their trip.\n"
        )
    ]

    Flights: Annotated[
        str,
        ...,
        (
            "Flights:\n"
            "\nThis section provides details on available flights, including recommended airlines, "
            "flight durations, and any travel tips for reaching the destination.\n"
        )
    ]

