from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from app.api.routes.chat import router as chat_router
from app.api.routes.dashboard import router as dashboard_router
from app.api.routes.demo import router as demo_router
from app.api.routes.handoffs import router as handoffs_router
from app.api.routes.leads import router as leads_router
from app.api.routes.ui import router as ui_router
from app.db.models import Base
from app.db.session import engine

app = FastAPI(title="MechanicFlow AI")

Base.metadata.create_all(bind=engine)

app.include_router(chat_router)
app.include_router(leads_router)
app.include_router(handoffs_router)
app.include_router(dashboard_router)
app.include_router(demo_router)
app.include_router(ui_router)


@app.get("/")
def root():
    return RedirectResponse(url="/ui")


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
