import json
import os

from fastapi import Request
from dotenv import load_dotenv


def load_config():
    with open("config.json", "r") as f:
        config = json.load(f)
    return config


def requires_auth():
    config = load_config()
    return config["require_auth"]


def is_validated(request: Request):
    load_dotenv()
    if not requires_auth():
        return True
    token = os.getenv("AUTH_TOKEN")
    auth_header = request.headers.get("Authorization")
    if not auth_header or len(auth_header.split(" ")) != 2:
        return False
    auth_header_split = auth_header.split(" ")
    if auth_header_split[0] != "Bearer":
        return False
    if auth_header_split[1] != token:
        return False
    return True
