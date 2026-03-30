from fastapi import FastAPI
from app.routes import router
app = FastAPI(title="AI Text Enhancer API")
app.include_router(router)
