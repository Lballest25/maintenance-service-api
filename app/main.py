from fastapi import FastAPI

from app.api.v1.category_routes import router as category_router
from app.api.v1.item_routes import router as item_router
from app.api.v1.order_routes import router as order_router
from app.core.config import settings
# Comentar la siguiente línea para ejecutar pruebas
from app.core.database import Base, engine

app = FastAPI(title=settings.APP_NAME)

# Comentar la siguiente línea para ejecutar pruebas,
# simplemente sirve para crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

app.include_router(item_router)
app.include_router(order_router)
app.include_router(category_router)
