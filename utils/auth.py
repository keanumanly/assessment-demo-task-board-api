import os
from fastapi import HTTPException, Depends
from fastapi.security import APIKeyHeader
from dotenv import load_dotenv

load_dotenv()

APIKEY = os.getenv("APIKEY")

# Define API key security scheme
api_key_scheme = APIKeyHeader(name="Authorization")


async def authenticate(api_key: str = Depends(api_key_scheme)):
    if api_key != APIKEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return api_key
