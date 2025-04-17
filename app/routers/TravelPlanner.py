from fastapi import Depends, APIRouter
from app.models import model_type as model
from app.utils.graph import run_graph
from app.helpers.auth_helper import verify_access_token

router = APIRouter()

@router.get("/")
async def read_root():
    return {"message": "Welcome to the Lesson Plan API!"}

@router.post("/travel_planner")
async def create_trip_plan(
    request: model.TripPlanRequest = Depends(),
    user: dict = Depends(verify_access_token)
):
    print("1")
    try:
        Travel_Plan = await run_graph(request) 
        return {
            "status": "success",
            "message": "Travel Plan Generated Successfully",
            "data": Travel_Plan
            
        }
    except Exception as e: 
        return f"Error {e}"