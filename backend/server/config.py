import os

from starlette.datastructures import Secret
from fastapi_users.authentication import JWTAuthentication

# APP Stuff
DEBUG = os.getenv("DEBUG", True)
SECRET_KEY = "secret"

ALLOWED_HOSTS = [
    "*",
]

jwt_authentication = JWTAuthentication(
    secret=SECRET_KEY, lifetime_seconds=3600 * 365, tokenUrl="auth/login"
)
AUTH_BACKENDS = [jwt_authentication]

# DB Stuff
MONGO_ENDPOINT = os.getenv(
    "MONGO_ENDPOINT", "mongodb://aeturnum:aeturnum@0.0.0.0:27018"
)
DB_NAME = "aeturnumdb"

# Superuser stuff
SUPERUSER_EMAIL = os.getenv("SUPERUSER_EMAIL", "admin@aeturnum.ai")
SUPERUSER_PASSWORD = os.getenv("SUPERUSER_PASSWORD", "password")
