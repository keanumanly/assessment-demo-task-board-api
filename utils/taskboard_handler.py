
from fastapi import HTTPException
from models.schema_api import PostingData
from dotenv import load_dotenv
import json
import redis
import os

load_dotenv()
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = int(os.getenv("REDIS_PORT"))
REDIS_DB = int(os.getenv("REDIS_DB"))

# Set & Connect the Redis Client
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)


def get_request():
    try:
        result = json.loads(redis_client.get("TASKS"))
        return result
    except Exception as e:
        print(f"❌ Error: {e}")
        raise HTTPException(status_code=404, detail=f"{str(e)}")


def post_request(response_model: PostingData):
    try:
        data = response_model.model_dump()
        if data.get("id") is None or not data.get("id"):
            raise HTTPException(status_code=404, detail="No Data")
        taks_list = json.loads(redis_client.get("TASKS"))
        taks_list[data["id"]] = data
        json_object = json.dumps(taks_list)
        redis_client.set("TASKS", json_object)
        return taks_list
    except Exception as e:
        print(f"❌ Error: {e}")
        raise HTTPException(status_code=404, detail=f"{str(e)}")


def put_request(response_model: PostingData):
    try:
        data = response_model.model_dump()
        if data.get("id") is None or not data.get("id"):
            raise HTTPException(status_code=404, detail="No Data")
        taks_list = json.loads(redis_client.get("TASKS"))
        taks_list[data["id"]] = data
        json_object = json.dumps(taks_list)
        redis_client.set("TASKS", json_object)
        return taks_list
    except Exception as e:
        print(f"❌ Error: {e}")
        raise HTTPException(status_code=404, detail=f"{str(e)}")


def del_request(uuid: str):
    try:
        taks_list = json.loads(redis_client.get("TASKS"))
        del taks_list[uuid]
        json_object = json.dumps(taks_list)
        redis_client.set("TASKS", json_object)
        return taks_list
    except Exception as e:
        print(f"❌ Error: {e}")
        raise HTTPException(status_code=404, detail=f"{str(e)}")


def execute_label_request():
    try:
        result = json.loads(redis_client.get("LABELS"))
        return result
    except Exception as e:
        print(f"❌ Error: {e}")
        raise HTTPException(status_code=404, detail=f"{str(e)}")


def execute_assignees_request():
    try:
        result = json.loads(redis_client.get("ASSIGNEES"))
        return result
    except Exception as e:
        print(f"❌ Error: {e}")
        raise HTTPException(status_code=404, detail=f"{str(e)}")
