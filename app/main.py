from fastapi import FastAPI, Depends
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
# from fastapi.openapi.utils import get_openapi
# from app.utils.custom_api import custom_api

from app.database import engine, Base
from app.configs.config import settings
from app.utils.auth import authenticate
# from app.routes.router import router
from app.routes import assignees, labels, tasks, auth as auth_router
import app.models.models
from app.configs.dependencies import get_current_active_user

# root = os.getenv("ROOT_PATH", "")
# root = "/"  # local test
root = ""


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="""
## FastAPI CRUD App

A production-ready REST + GraphQL API featuring:

- 🔐 **JWT Authentication** — register, login, bearer token protection
- 📦 **Items CRUD** — create, read, update, delete your items
- 👤 **User Management** — profile retrieval and updates
- 🔍 **PostgreSQL** — flexible queries and mutations via Strawberry
- 📄 **Auto Docs** — Swagger UI at `/docs`, ReDoc at `/redoc`
    """,
    # root_path=root,
    # redoc_url="/redoc",
    # docs_url="/docs"
)

origins = ["*"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(auth_router.router)
app.include_router(assignees.router, dependencies=[Depends(get_current_active_user)])
app.include_router(labels.router, dependencies=[Depends(get_current_active_user)])
app.include_router(tasks.router, dependencies=[Depends(get_current_active_user)])


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")


@app.get("/health", tags=["Health"])
async def health():
    return {"status": "ok"}


# def custom_openapi():
#     # cache the generated schema
#     if app.openapi_schema:
#         return app.openapi_schema

#     # custom settings
#     openapi_schema = get_openapi(
#         title="Assessment Demo Task Board API",
#         version="0.0.1",
#         description="This api is serve as Demo API",
#         routes=app.routes,
#     )
#     if root:
#         app.openapi_schema = custom_api(openapi_schema, path=root)
#     app.openapi_schema = openapi_schema
#     return app.openapi_schema


# app.openapi = custom_openapi
