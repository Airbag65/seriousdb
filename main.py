import pickle
import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request, status
from fastapi import HTTPException
from fastapi.responses import JSONResponse

from auth import is_validated, require_auth

db_file = ".sdb"

# Check if the database file exists, if not populate it
if not os.path.isfile(db_file):
    with open(db_file, "wb") as f:
        pickle.dump({"default": "default"}, f)
    f.close()

app = FastAPI()

if not load_dotenv():
    if require_auth:
        raise RuntimeError(".env must exist and contain 'AUTH_TOKEN'")


@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    if not is_validated(request):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED, content={"status": "Unauthorized"}
        )
    response = await call_next(request)
    return response


@app.put("/db")
async def put(key: str, value: str):
    db = None
    with open(db_file, "rb") as f:
        db = pickle.load(f)
        db[key] = value
    f.close()
    with open(db_file, "wb+") as f:
        pickle.dump(db, f)
    f.close()
    return value


@app.get("/db")
async def get(key: str):
    db = None
    with open(db_file, "rb") as f:
        db = pickle.load(f)
    f.close()
    if db is None:
        raise HTTPException(
            status_code=404,
            detail=f"Database file {db_file} could not be opened and loaded",
        )
    val = db.get(key, None)
    if val is None:
        raise HTTPException(status_code=404, detail=f"No value set for key {key}")
    return val
