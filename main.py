import os
from dotenv import load_dotenv
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from starlette_wtf import CSRFProtectMiddleware
# Custom middlewares
from middlewares.logging_middleware import LoggingMiddleware
from middlewares.rate_limit_middleware import RateLimitMiddleware
from middlewares.security_headers_middleware import SecurityHeadersMiddleware
from routers.users_router import users_router
from routers.mails_router import mails_router
from routers.otp_router import otp_router
from models.users_model import Base
from database.connection import engine

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(users_router)
app.include_router(mails_router)
app.include_router(otp_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=['*'])
# app.add_middleware(HTTPSRedirectMiddleware)
app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(LoggingMiddleware)
app.add_middleware(CSRFProtectMiddleware, csrf_secret=os.getenv('CSRF_SECRET_KEY'))
app.add_middleware(RateLimitMiddleware, max_requests=10, window_seconds=60)
app.add_middleware(SecurityHeadersMiddleware)

