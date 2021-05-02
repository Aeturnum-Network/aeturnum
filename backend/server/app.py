from fastapi import FastAPI, Depends
from fastapi_users import FastAPIUsers
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware

from server.config import *
from server.database import *
from server.routes.assets import router as assets_router
from server.routes.users import router as users_router
from server.routes.users import fastapi_users

app = FastAPI(
    title="Aeturnum API",
    description="End to End API interface for Aeturnum",
    version="0.1.0",
    docs_url="/",
    # root_path="/api",
)

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex="https?://.*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_event_handler("startup", connect_to_mongo)
app.add_event_handler("startup", init_superuser)
app.add_event_handler("shutdown", close_mongo_connection)


# User Routes
app.include_router(
    fastapi_users.get_auth_router(AUTH_BACKENDS[0]), prefix="/auth", tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(),
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(fastapi_users.current_user(active=True, superuser=True))],
)
# app.include_router(
#     fastapi_users.get_reset_password_router(SECRET_KEY), prefix="/auth", tags=["auth"]
# )
app.include_router(fastapi_users.get_users_router(), prefix="/users", tags=["users"])

# Asset Routes
app.include_router(assets_router, prefix="/assets", tags=["assets"])

# User custom route
app.include_router(users_router, prefix="/users", tags=["users"])
