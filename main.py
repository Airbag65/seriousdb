import json
import os
from fastapi import FastAPI
from fastapi import HTTPException
from threading import Lock

class Cache:
    def __init__(self):
        self.filename = None
        self.db = None
        self.lock = Lock()


def insert(key: str, value: str, cache: Cache):
    with cache.lock:  
        if cache.db is None:
            raise HTTPException(status_code=404, detail=f"Database file {cache.filename} could not be opened and loaded")
        cache.db[key] = value
    return value


def select(key: str, cache: Cache):
    with cache.lock: 
        if cache.db is None:
            raise HTTPException(status_code=404, detail=f"Database file {cache.filename} could not be opened and loaded")
        val = cache.db.get(key, None)
    if val is None:
        raise HTTPException(status_code=404, detail=f"No value set for key {key}")
    return val


def load(filename: str, cache: Cache):
    with cache.lock:  
        db_file = filename
        if not os.path.isfile(db_file):
            with open(db_file, "wb") as f:
                json_dumps = json.dumps({"default": "default"}).encode()
                f.write(json_dumps)
            cache.db = {"default": "default"}
        else:
            with open(filename, "rb") as f:
                binary_text = f.read()
                json_text = binary_text.decode()
                cache.db = json.loads(json_text)
        cache.filename = filename


def flush(cache: Cache):
    with cache.lock:  
        if cache.db is None:
            return
        with open(cache.filename, "wb+") as f:
            json_dumps = json.dumps(cache.db).encode()
            f.write(json_dumps)


db_file = ".sdb"

# Check if the database file exists, if not populate it
if not os.path.isfile(db_file):
    with open(db_file, "wb") as f:
        json_dumps = json.dumps({"default": "default"}).encode()
        f.write(json_dumps)

app = FastAPI()


@app.put("/db")
async def put(key: str, value: str):
    db = None
    with open(db_file, "rb") as f:
        binary_text = f.readline()
        json_text = binary_text.decode()
        db = json.loads(json_text)
        db[key] = value
    with open(db_file, "wb+") as f:
        json_dumps = json.dumps(db).encode()
        f.write(json_dumps)
    return value


@app.get("/db")
async def get(key: str):
    db = None
    with open(db_file, "rb") as f:
        db = json.load(f)
    if db is None:
        raise HTTPException(
            status_code=404,
            detail=f"Database file {db_file} could not be opened and loaded",
        )
    val = db.get(key, None)
    if val is None:
        raise HTTPException(status_code=404, detail=f"No value set for key {key}")
    return val
