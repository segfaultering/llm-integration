from fastapi import FastAPI, status

from llm_integration.routes import router

app = FastAPI()
app.include_router(router)


@app.get("/", status_code=status.HTTP_200_OK, response_model=str)
def read_root() -> str:
    return "Hello World!"
