from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS
import turso_serverless


app = application = Flask(__name__)
app.config.from_object('config')

CORS(app, origins=[
    "http://localhost:5173", "https://ai-rag-two.vercel.app"
])

def turso_conn():
    conn = turso_serverless.connect(
        app.config.get("TURSO_DATABASE_URL"),
        auth_token=app.config.get("TURSO_AUTH_TOKEN")
    )
    return conn

api = Api(app, catch_all_404s=True)