from fastapi import FastAPI

from src.urls import router

app = FastAPI()
app.include_router(
    router,
    prefix="/car",
    tags=["car"],
)


@app.get("/")
async def root():
    return {"msg": "Welcome to Car Reservation System!"}
