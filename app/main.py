import uvicorn
from app.routers import TravelPlanner  # Import the travelplan router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the travelplan router
app.include_router(TravelPlanner.router, tags=["TravelPlan"], prefix="/travelplan")

@app.get("/health")
async def root():
    return {"message": "API is working fine."}

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app", host="127.0.0.1", port=8090, log_level="info", reload=True
    )