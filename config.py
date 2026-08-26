import os

SECRET_KEY = os.environ.get("SECRET_KEY", "fallback-secret-string")

TURSO_DATABASE_URL = os.environ.get("TURSO_DATABASE_URL", "local_database.db")
TURSO_AUTH_TOKEN = os.environ.get("TURSO_AUTH_TOKEN", "")

MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/future_database")

JWT_SECRET = os.environ.get("JWT_SECRET")