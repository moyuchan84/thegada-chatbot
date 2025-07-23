
from fastapi import FastAPI
from controller.router import math_router
from controller.router import test_router
from controller.router import validate_router

app = FastAPI()

app.include_router(math_router.router, prefix="/api/math", tags=["math"])

app.include_router(test_router.router, prefix="/api/test", tags=["test"])
app.include_router(validate_router.router, prefix="/api/validate", tags=["validate"])
@app.get("/")
async def read_root():
    return {"Hello": "World"}
