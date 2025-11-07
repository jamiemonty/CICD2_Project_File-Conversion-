from fastapi import FastAPI
from routes import convert


app = FastAPI(
    title="File Conversion Microservice",
    description="Handles file uploads, conversion, and optional content filtering."
)

app.include_router(convert.router, prefix="/api/v1/convert", tags=["Conversion"])

@app.get("/")
def index():
    # Example root endpoint to check health
    return {"message": "Welcome to the File Conversion Service!"}