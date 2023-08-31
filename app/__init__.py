from telegram.ext import ApplicationBuilder
import os
import json
from dotenv import load_dotenv
from sqlalchemy import create_engine

import yaml

from telegram import (
    Update, InlineKeyboardButton, KeyboardButton, 
    ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup,   
)
from telegram.ext import (
    ApplicationBuilder, ContextTypes, CommandHandler, 
    filters, MessageHandler, CallbackQueryHandler,
    ConversationHandler
)

import logging

__all__ = [
    "Update", "InlineKeyboardButton", "KeyboardButton",
    "ReplyKeyboardMarkup", "ReplyKeyboardRemove", "InlineKeyboardMarkup",
    "ContextTypes", "CommandHandler", "filters", "MessageHandler",
    "CallbackQueryHandler", "ConversationHandler",
    "config", "build_app", "static_text", "engine",
]

load_dotenv()

def config():
    with open("app/config.yml", "r") as c: #* there's a hardcode here 
        config = yaml.safe_load(c)
    return config

def build_app():
    application = ApplicationBuilder()\
        .token(os.getenv("TOKEN"))\
        .build()
    return application

def static_text():
    
    with open("app/text_data.json", "r") as f: #* there's a hardcode here
        data = json.loads(f.read())
        return data

def engine():
    engine = create_engine(
        "postgresql+psycopg2://"
        + f"{os.getenv('POSTGRES_USER')}:"
        + f"{os.getenv('POSTGRES_PASSWORD')}@"
        + f"{os.getenv('HOST')}/{os.getenv('POSTGRES_DB')}",
        echo=True
    )
    
    return engine

def logger():
    print("Called")
    logger = logging.getLogger("CLIENTS")
    logging.basicConfig(level=logging.INFO)

    basic_file_handler = logging.FileHandler("file.log")

    log_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    basic_file_handler.setFormatter(log_format)

    logger.addHandler(basic_file_handler)

    return logger