from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from utils.custom_api import custom_api
from api.router import router

# root = os.getenv("ROOT_PATH", "")
# root = "/"  # local test
root = ""


app = FastAPI(
    title="Assessment Demo Task Board API",
    version="0.0.1",
    root_path=root,
    redoc_url="/redoc",
    docs_url="/docs"
)

origins = ["*"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/", include_in_schema=False)
def redirect_to_docs():
    return RedirectResponse(url="/docs")


def custom_openapi():
    # cache the generated schema
    if app.openapi_schema:
        return app.openapi_schema

    # custom settings
    openapi_schema = get_openapi(
        title="Assessment Demo Task Board API",
        version="0.0.1",
        description="This api is serve as Demo API",
        routes=app.routes,
    )
    if root:
        app.openapi_schema = custom_api(openapi_schema, path=root)
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
