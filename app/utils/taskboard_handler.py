
from fastapi import HTTPException
from models.schema_api import PostingData
from configs.config import settings
import json


def get_request():
    try:
        result = json.loads(settings.REDIS_CLIENT.get("TASKS"))
        return result
    except Exception as e:
        print(f"❌ Error: {e}")
        raise HTTPException(status_code=404, detail=f"{str(e)}")


def post_request(response_model: PostingData):
    try:
        data = response_model.model_dump()
        if data.get("id") is None or not data.get("id"):
            raise HTTPException(status_code=404, detail="No Data")
        taks_list = json.loads(settings.REDIS_CLIENT.get("TASKS"))
        taks_list[data["id"]] = data
        json_object = json.dumps(taks_list)
        settings.REDIS_CLIENT.set("TASKS", json_object)
        return taks_list
    except Exception as e:
        print(f"❌ Error: {e}")
        raise HTTPException(status_code=404, detail=f"{str(e)}")


def put_request(response_model: PostingData):
    try:
        data = response_model.model_dump()
        if data.get("id") is None or not data.get("id"):
            raise HTTPException(status_code=404, detail="No Data")
        taks_list = json.loads(settings.REDIS_CLIENT.get("TASKS"))
        taks_list[data["id"]] = data
        json_object = json.dumps(taks_list)
        settings.REDIS_CLIENT.set("TASKS", json_object)
        return taks_list
    except Exception as e:
        print(f"❌ Error: {e}")
        raise HTTPException(status_code=404, detail=f"{str(e)}")


def del_request(uuid: str):
    try:
        taks_list = json.loads(settings.REDIS_CLIENT.get("TASKS"))
        del taks_list[uuid]
        json_object = json.dumps(taks_list)
        settings.REDIS_CLIENT.set("TASKS", json_object)
        return taks_list
    except Exception as e:
        print(f"❌ Error: {e}")
        raise HTTPException(status_code=404, detail=f"{str(e)}")


def execute_label_request():
    try:
        result = json.loads(settings.REDIS_CLIENT.get("LABELS"))
        return result
    except Exception as e:
        print(f"❌ Error: {e}")
        raise HTTPException(status_code=404, detail=f"{str(e)}")


def execute_assignees_request():
    try:
        result = json.loads(settings.REDIS_CLIENT.get("ASSIGNEES"))
        return result
    except Exception as e:
        print(f"❌ Error: {e}")
        raise HTTPException(status_code=404, detail=f"{str(e)}")
