# Travel Planner API

AI-powered itinerary builder that assembles end-to-end travel plans using LangGraph orchestration, LangChain agents, and external search providers. The service consumes a small set of traveler preferences and returns a structured itinerary with day-by-day activities, dining, flights, and hotel links.

## Key Features
- AI-generated destination overview, activity list, and dining suggestions tuned to traveler interests.
- Automated enrichment with hotel links, curated travel guides, and flight options via SerpAPI and Google Serper.
- LangGraph state machine that sequences independent agents (destination detail → places → activities → dining → hotels/links → flights → final assembly).
- FastAPI backend with JWT-style bearer token verification hook for secure access.

## Architecture Overview
- `FastAPI` app (`app/main.py`) exposes REST endpoints and configures CORS.
- `app/routers/TravelPlanner.py` orchestrates requests, validates payloads, and triggers the graph pipeline.
- `app/models/model_type.py` defines request/response schemas and LangGraph state (`TripPlanState`, `AssembledTravelPlan`).
- `app/utils/graph.py` builds and runs the LangGraph `StateGraph`, chaining async nodes for each planning phase.
- `app/utils/agent.py` contains LangChain-powered agents that talk to OpenAI's `gpt-4o` model and return structured outputs.
- `app/utils/{hotel,links,flight}.py` call Google Serper and SerpAPI to enrich AI output with real-world data.
- `app/helpers/auth_helper.py` verifies access tokens against an external auth service defined by `VERIFY_TOKEN_URL`.

## Tech Stack
- Python 3.10+
- FastAPI & Uvicorn
- LangChain, LangGraph
- OpenAI GPT-4o (via `langchain-openai`)
- SerpAPI (Google Flights) and Google Serper API
- Pydantic v1

## Prerequisites
- Python 3.10 or newer
- OpenAI API key with access to `gpt-4o`
- SerpAPI key for Google Flights search
- Serper API key for Google search results
- Token verification service URL (for bearer token validation)

## Installation
```bash
git clone <repo-url> Travel_Planner
cd Travel_Planner
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS/Linux
pip install --upgrade pip
pip install -r requirements.txt
```

## Environment Variables
Create a `.env` file in the project root:
```
YOUR_OPENAI_API_KEY=<openai-api-key>
SERPAPI_KEY=<serpapi-key>
SERPER_API_KEY=<google-serper-api-key>
VERIFY_TOKEN_URL=<https-endpoint-that-validates-access-tokens>
```

> The Google Serper and SerpAPI keys are required for hotel/guide search and flight enrichment respectively.

## Running the API
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Alternatively, use the helper script:
```bash
python start.py
```

The service exposes a health endpoint at `GET /health`.

## Authentication
All itinerary endpoints are protected by bearer token auth:
- Include `Authorization: Bearer <token>` with each request.
- Tokens are verified via `VERIFY_TOKEN_URL`; make sure the URL returns HTTP 200 for valid tokens.

## API Reference

### `GET /health`
Sanity check endpoint.

### `POST /travelplan/travel_planner`
Generates a travel itinerary.

**Headers**
- `Authorization: Bearer <token>`
- `Content-Type: application/json`

**Request Body**
```json
{
  "Destination": "Kyoto, Japan",
  "Duration": 5,
  "Number_of_People": 2,
  "Traveling_With": "Partner",
  "Interests": "Culture, food, outdoor activities",
  "Itinerary_Style": "Relaxed",
  "Budget": "mid-range",
  "Departure_id": "SFO",
  "Arrival_id": "KIX",
  "Date": "2025-03-15"
}
```

**Successful Response (abridged)**

```json
{
  "status": "success",
  "message": "Travel Plan Generated Successfully",
  "data": [
    {
      "Destination_Overview": "...",
      "Day_by_Day_Plan": "...",
      "Recommended_Links": "...",
      "Flights": "..."
    }
  ]
}
```

Errors return a JSON object with an `error` or `detail` field.

## Development Tips
- Update prompts in `app/utils/prompt.py` to tweak tone or structure of AI responses.
- Add new graph nodes in `app/utils/graph.py` for extra enrichment steps (e.g., weather, local tips).
- Use FastAPI's interactive docs at `http://localhost:8000/docs` to test endpoints when running locally.

## Deployment Notes
- `appspec.yml` and scripts in `scripts/` are provided for automated deployment (e.g., AWS CodeDeploy).
- Ensure environment variables are configured in the target hosting environment.

## Contributing
1. Fork & clone the repository.
2. Create a feature branch.
3. Add tests or sample responses where relevant.
4. Submit a pull request with clear summary and testing notes.

## License
Specify your preferred license in this section if applicable.
