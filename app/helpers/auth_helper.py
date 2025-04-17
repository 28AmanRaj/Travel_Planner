from fastapi import FastAPI, Depends, HTTPException, Request, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import httpx
import os

VERIFY_TOKEN_URL = os.getenv("VERIFY_TOKEN_URL")
security = HTTPBearer()

async def verify_access_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                VERIFY_TOKEN_URL,
                headers={"Authorization": f"Bearer {token}", "accept": "application/json"},
            )
            if response.status_code != 200:
                raise HTTPException(status_code=401, detail="Token verification failed")
            return response.json()  # User data or success response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")