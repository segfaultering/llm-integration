import logging

from fastapi import FastAPI, status

from llm_integration.constants import ENCODING, LOG_FILE, Paths
from llm_integration.routes import router

logging.basicConfig(
    # Log filed
    filename=(Paths.LOGS_DIR.value / LOG_FILE),
    encoding=ENCODING,
    filemode="a",
    level=logging.DEBUG
)

app = FastAPI()
app.include_router(router)


@app.get("/", status_code=status.HTTP_200_OK, response_model=str)
def read_root() -> str:
    return "Hello World!"
