from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routers import profile

app = FastAPI(title="FastAPI Final Project Application")

# Mount static files directory so profile.html can be served
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include the profile router
app.include_router(profile.router)

@app.get("/")
def read_root():
    return {"message": "API is running. Visit /static/profile.html to view your profile page."}