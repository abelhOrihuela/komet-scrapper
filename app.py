from flask import Flask
from flask_restful import Resource, Api
from db import db
from dotenv import load_dotenv

from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from lib.scrapper import main

load_dotenv()

def hello_job():
    with app.app_context():
        main()


class HelloWorld(Resource):
    def get(self):
        return {"hello": "world"}


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///komet_bot.db"

    app.app_context().push()
    api = Api(app)

    scheduler = BackgroundScheduler()
    scheduler.add_job(hello_job, trigger="interval", seconds=500)
    scheduler.start()

    db.init_app(app)
    db.create_all()

    try:
        return app
    except:
        scheduler.shutdown()


app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=5000, use_reloader=False)
