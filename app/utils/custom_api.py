def custom_api(openapi_schema, path="/"):
    openapi_schema["servers"] = [{"url": path}]
    # setting new logo to docs
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }

    return openapi_schema
