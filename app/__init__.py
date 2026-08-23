from flask import Flask
from flask_restful import Resource, Api
import turso_serverless


app = application = Flask(__name__)
app.config.from_object('config')

def turso_conn():
    conn = turso_serverless.connect(
        app.config.get("TURSO_DATABASE_URL"),
        auth_token=app.config.get("TURSO_AUTH_TOKEN")
    )
    return conn

api = Api(app, catch_all_404s=True)