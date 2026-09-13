import uvicorn

from seriousdb.configuration import get_configuration

if __name__ == "__main__":
    config = get_configuration()
    uvicorn.run("seriousdb.main:app", host="0.0.0.0", port=config.port, reload=True)
