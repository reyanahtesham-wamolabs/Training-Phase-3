from fastapi import FastAPI
from routes import router
from WS import ws_router
from mid import mid1
App=FastAPI()
App.middleware("http")(mid1)
App.include_router(router)
App.include_router(ws_router)
