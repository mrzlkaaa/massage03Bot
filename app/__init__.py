from telegram.ext import ApplicationBuilder
import os
from dotenv import load_dotenv

load_dotenv()


def build_app():
    application = ApplicationBuilder()\
        .token(os.getenv("TOKEN"))\
        .build()
    return application