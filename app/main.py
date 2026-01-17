from fastapi import FastAPI

from app.core.config import settings
from app.core.database import Base, engine
from app.api.v1.item_routes import router as item_router
from app.api.v1.category_routes import router as category_router

app = FastAPI(title=settings.APP_NAME)

Base.metadata.create_all(bind=engine)

app.include_router(item_router)
app.include_router(category_router)
