
from fastapi import FastAPI
from controller.router import math_router

app = FastAPI()

app.include_router(math_router.router, prefix="/api/math", tags=["math"])

@app.get("/")
async def read_root():
    return {"Hello": "World"}
