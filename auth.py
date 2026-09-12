import os

from fastapi import Request
from dotenv import load_dotenv

from configuration import CONFIG


def is_validated(request: Request) -> bool:
    if not CONFIG.require_auth:
        return True
    token = os.getenv("AUTH_TOKEN")
    auth_header = request.headers.get("Authorization")
    if not auth_header or len(auth_header.split(" ")) != 2:
        return False
    auth_header_split = auth_header.split(" ")
    if auth_header_split[0] != "Bearer":
        return False
    return auth_header_split[1] == token
