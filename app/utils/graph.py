from langgraph.graph import StateGraph, START
from app.models import model_type as models
from app.utils.agent import generate_destination_detail, place_recommendation, activity_recommendation, travel_plan_assembly



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
        state["Place_Recommendation"] = recommended_place
        print("Place recommendation generated successfully!")
        return state

    async def activity_recommendation_callback(state: models.TripPlanState):
        print("Generating activity recommendation...")
        recommended_activity = await activity_recommendation(state)
        state["Activity_Recommendation"] = recommended_activity
        print("Activity recommendation generated successfully!")
        return state

    async def travel_plan_assembly_callback(state: models.TripPlanState):
        print("Assembling travel plan...")
        travel_plan = await travel_plan_assembly(state)
        print("Travel plan assembled successfully!")
        state["Travel_Plan"] = travel_plan
        return state
    
    builder.add_node("Destination Detail", generate_destination_detail_callback)
    builder.add_node("Place Recommendation", place_recommendation_callback)
    builder.add_node("Activity Recommendation", activity_recommendation_callback)
    builder.add_node("Travel Plan Assembly", travel_plan_assembly_callback)


    builder.add_edge(START, "Destination Detail")
    builder.add_edge("Destination Detail", "Place Recommendation")
    builder.add_edge("Place Recommendation", "Activity Recommendation")
    builder.add_edge("Activity Recommendation", "Travel Plan Assembly")
    print("Travel plan graph built successfully!")

    travel_plan_graph = builder.compile()
    return travel_plan_graph



travel_plan_graph = graph_struct()


async def run_graph(request: models.TripPlanRequest):
    try:
        print("Running travel plan graph...")
        state = models.TripPlanState(Destination=request.Destination, Duration=request.Duration, Number_of_People=request.Number_of_People, Traveling_With=request.Traveling_With, Interests=request.Interests, Itinerary_Style=request.Itinerary_Style, Budget=request.Budget, Destination_Detail=" ", Place_Recommendation=" ", Activity_Recommendation=" ", Travel_Plan=" ")
        result = await travel_plan_graph.ainvoke(state)
        print("Travel plan graph execution completed!")
        return result["Travel_Plan"]
    except Exception as e:
         return {"error": str(e)}
    
# from IPython.display import Image, display

# try:
#     display(Image(travel_plan_graph.get_graph().draw_mermaid_png()))
# except Exception:
#     pass