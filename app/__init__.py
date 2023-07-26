from telegram.ext import ApplicationBuilder
import os
import json
from dotenv import load_dotenv

load_dotenv()


def build_app():
    application = ApplicationBuilder()\
        .token(os.getenv("TOKEN"))\
        .build()
    return application

def static_text():
    print(os.listdir())
    with open("app/text_data.json", "r") as f:
        data = json.loads(f.read())
        return data