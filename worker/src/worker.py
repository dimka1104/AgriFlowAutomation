from fastapi import FastAPI

from agriflow.routes_admin import router as admin_router
from agriflow.routes_auth import router as auth_router
from agriflow.routes_main import router as main_router

app = FastAPI(title="AgriFlow API")
app.include_router(auth_router)
app.include_router(main_router)
app.include_router(admin_router)


import asgi

Default = asgi.entrypoint(app)
