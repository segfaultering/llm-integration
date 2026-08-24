from fastapi import FastAPI, status
import uvicorn


app = FastAPI()


@app.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=str
)
def read_root() -> str:
    return "Hello World!"
