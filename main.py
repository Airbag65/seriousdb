import json
import os
from fastapi import FastAPI
from fastapi import HTTPException

db_file = ".sdb"

# Check if the database file exists, if not populate it
if not os.path.isfile(db_file):
    with open(db_file, "wb") as f:
        json_dumps = json.dumps({"default": "default"}).encode()
        f.write(json_dumps)
    f.close()

app = FastAPI()


@app.put("/db")
async def put(key: str, value: str):
    db = None
    with open(db_file, "rb") as f:
        db = json.load(f)
        db[key] = value
    f.close()
    with open(db_file, "wb+") as f:
        json_dumps = json.dumps(db).encode()
        f.write(json_dumps)
    f.close()
    return value


@app.get("/db")
async def get(key: str):
    db = None
    with open(db_file, "rb") as f:
        db = json.load(f)
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
