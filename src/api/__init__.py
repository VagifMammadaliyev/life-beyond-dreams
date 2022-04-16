from fastapi import FastAPI

from api.urls import router


app = FastAPI()
app.include_router(router)
