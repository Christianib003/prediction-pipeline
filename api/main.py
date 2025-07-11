from fastapi import FastAPI
from app import routes

# Create the FastAPI app instance
app = FastAPI(
    title="Plant Disease API",
    description="API for accessing plant disease dataset metadata.",
    version="1.0.0"
)

# Include the router from the routes module
app.include_router(routes.router)

@app.get("/")
def read_root():
    """A simple root endpoint to confirm the API is running."""
    return {"message": "Welcome to the Plant Disease API!"}
