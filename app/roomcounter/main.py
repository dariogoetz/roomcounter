from fastapi import FastAPI, Depends, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from roomcounter.api.api import api_router
from roomcounter.core.config import settings
from roomcounter.core.templating import templates, default_template_context
from roomcounter.api.dependencies import admin
from roomcounter.schemas.user import AuthenticatedUser
from roomcounter.db.init_db import init_database

app = FastAPI(title=settings.APP_NAME)

app.include_router(api_router)
app.mount("/static",
          StaticFiles(directory="roomcounter/static"), name="static")


init_database()


@app.get("/", response_class=HTMLResponse)
async def home(request: Request,
               context: dict = Depends(default_template_context)):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, **context}
    )
