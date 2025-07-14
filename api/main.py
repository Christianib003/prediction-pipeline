from fastapi import FastAPI
from .app import routes

app = FastAPI(
    title="Plant Disease API",
    description="API for accessing and managing plant disease data.",
    version="1.0.0"
)

app.include_router(routes.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Plant Disease API!"}