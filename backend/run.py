from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi_jwt import JwtAuthorizationCredentials, JwtAccessBearer
from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request
from app.routes.users import router as user_router

from app.routes.projects import router as project_router

app = FastAPI(title="AI Discovery Assistant", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# JWT dependency setup
jwt = JwtAccessBearer(secret_key="your-secret-key", auto_error=True)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()},
    )

# Include your routers
app.include_router(user_router)
app.include_router(project_router)
