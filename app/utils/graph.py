from langgraph.graph import StateGraph, START
from app.models import model_type as models
from app.utils.agent import generate_destination_detail, place_recommendation, activity_recommendation, travel_plan_assembly, dinning_recomendation
from app.utils.hotel import fetch_hotels
from app.utils.links import fetch_links
from app.utils.flight import get_flight_details

assembled_travel_plan = {}

def graph_struct():
    print("Building Travel plan graph...")
    builder = StateGraph(models.TripPlanState)

    async def generate_destination_detail_callback(state: models.TripPlanState):
        print("Generating destination detail...")
        destination_detail = await generate_destination_detail(state)
        state["Destination_Detail"] = destination_detail
        print("Destination detail generated successfully!")
        return state

    async def place_recommendation_callback(state: models.TripPlanState):
        print("Generating place recommendation...")
        recommended_place = await place_recommendation(state)
        state["Recommended_Places"] = recommended_place
        print("Place recommendation generated successfully!")
        return state
    
    async def dinning_recommendation_callback(state: models.TripPlanState):
        print("Generating dinning recommendation...")
        recommended_dinning = await dinning_recomendation(state)
        state["Recommended_dinning"] = {"recommendation": recommended_dinning}
        print("Dinning recommendation generated successfully!")
        return state


    async def activity_recommendation_callback(state: models.TripPlanState):
        print("Generating activity recommendation...")
        recommended_activity = await activity_recommendation(state)
        state["Recommended_Activity"] = recommended_activity
        print("Activity recommendation generated successfully!")
        return state
    
    async def link_recommendation(state: models.TripPlanState):
        print("Fetching links...")
        recommended_hotel = await fetch_hotels(state)
        famous_places = await fetch_links(state)
        state["Recommended_Hotels"] = recommended_hotel
        state["Recommended_Links"] = famous_places
        print("Recommended hotels: ", recommended_hotel)
        print("Famous places: ", famous_places)
        print("Links Fetched successfully!")
        return state
    
    async def get_flight_deatails_callback(state: models.TripPlanState):
        print("Fetching flights...")
        departure_id = state["Departure_id"]
        arrival_id = state["Arrival_id"]
        date = state["Date"]
        if departure_id and arrival_id and date:
            flights = await get_flight_details(departure_id=departure_id, arrival_id=arrival_id, date=date)
            print(flights)
            state["Recommended_flights"] = flights
            
        else:
            flights = {"Error": "Details not provided"}
            state["Recommended_flights"] = flights
    
        print("Flights fetched successfully!")
        return state



    async def travel_plan_assembly_callback(state: models.TripPlanState):
        print("Assembling travel plan...")
        travel_plan = await travel_plan_assembly(state)
        print("Travel plan assembled successfully!")
        assembled_travel_plan["travel_plan"] = travel_plan
        list_travel_plan = [ assembled_travel_plan["travel_plan"]]
        state["Travel_Plan"] = list_travel_plan
        return state
    
   
    
    builder.add_node("Destination Detail", generate_destination_detail_callback)
    builder.add_node("Place Recommendation", place_recommendation_callback)
    builder.add_node("Dinning Recommendation", dinning_recommendation_callback)
    builder.add_node("Activity Recommendation", activity_recommendation_callback)
    builder.add_node("Hotel Recommendation", link_recommendation)
    builder.add_node("Flight Details", get_flight_deatails_callback)
    builder.add_node("Travel Plan Assembly", travel_plan_assembly_callback)
   


    builder.add_edge(START, "Destination Detail")
    builder.add_edge("Destination Detail", "Place Recommendation")
    builder.add_edge("Place Recommendation", "Activity Recommendation")
    builder.add_edge("Activity Recommendation", "Dinning Recommendation")
    builder.add_edge("Dinning Recommendation", "Hotel Recommendation")
    builder.add_edge("Hotel Recommendation", "Flight Details")
    builder.add_edge("Flight Details", "Travel Plan Assembly")

    print("Travel plan graph built successfully!")

    travel_plan_graph = builder.compile()
    return travel_plan_graph



travel_plan_graph = graph_struct()


async def run_graph(request: models.TripPlanRequest):
    try:
        print("Running travel plan graph...")
        state = models.TripPlanState(Destination=request.Destination, Duration=request.Duration, Number_of_People=request.Number_of_People, Traveling_With=request.Traveling_With, Interests=request.Interests, Itinerary_Style=request.Itinerary_Style, Budget=request.Budget, Destination_Detail=" ", Recommended_Places=" ", Recommended_Activity=" ", Recommended_Hotels= {}, Recommended_Links={},Recommended_flights={},Recommended_dinning={}, Travel_Plan=[], Arrival_id=request.Arrival_id, Departure_id=request.Departure_id, Date=request.Date)
        result = await travel_plan_graph.ainvoke(state)
        print("Travel plan graph execution completed!")
        return result["Travel_Plan"]
    except Exception as e:
         return {"error": str(e)}
    