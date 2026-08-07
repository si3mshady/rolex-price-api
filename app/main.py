import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import (
    health_router,
    watches_router,
    collections_router,
    search_router,
    statistics_router,
)
from app.services.rolex_service import rolex_service, RolexNotFoundError
from app.schemas.error import ErrorResponse, ErrorDetail

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("rolex_price_api")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan context manager for startup and shutdown event handling.
    """
    logger.info("Initializing Rolex Price API service...")
    try:
        data_path = settings.resolve_data_path()
        logger.info(f"Loading watch catalog from {data_path}")
        # rolex_service initializes data automatically, log record count
        logger.info(f"Service loaded {rolex_service.watch_count} watches into memory.")
    except Exception as err:
        logger.error(f"Failed to load data on startup: {err}")

    yield

    logger.info("Shutting down Rolex Price API service...")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=settings.APP_DESCRIPTION,
    docs_url=settings.DOCS_URL,
    redoc_url=settings.REDOC_URL,
    openapi_url=settings.OPENAPI_URL,
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def verify_api_key_middleware(request: Request, call_next):
    """
    Validates X-Api-Key header when API_KEY_REQUIRED is enabled.
    Excluded open paths: /health, /docs, /redoc, /openapi.json, /.
    """
    if settings.API_KEY_REQUIRED:
        open_paths = {
            "/health",
            "/docs",
            "/redoc",
            "/openapi.json",
            "/favicon.ico",
            "/",
        }
        if request.url.path not in open_paths:
            api_key = request.headers.get("X-Api-Key")
            if not api_key or api_key != settings.API_KEY:
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content=ErrorResponse(
                        error=ErrorDetail(
                            code="UNAUTHORIZED",
                            message="Invalid or missing API Key. Provide a valid 'X-Api-Key' header.",
                        )
                    ).model_dump(),
                )
    return await call_next(request)


# Exception Handlers
@app.exception_handler(RolexNotFoundError)
async def rolex_not_found_handler(request: Request, exc: RolexNotFoundError):
    """Handle custom RolexNotFoundError exceptions."""
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=ErrorResponse(
            error=ErrorDetail(
                code="NOT_FOUND",
                message=exc.message,
            )
        ).model_dump(),
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle standard HTTP exceptions with structured response model."""
    code_map = {
        400: "BAD_REQUEST",
        404: "NOT_FOUND",
        422: "UNPROCESSABLE_ENTITY",
        500: "INTERNAL_SERVER_ERROR",
    }
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error=ErrorDetail(
                code=code_map.get(exc.status_code, "ERROR"),
                message=str(exc.detail),
            )
        ).model_dump(),
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle request validation errors with clear field breakdown."""
    errors_list = exc.errors()
    simplified_errors = []
    for err in errors_list:
        loc = " -> ".join([str(p) for p in err.get("loc", [])])
        simplified_errors.append({"location": loc, "msg": err.get("msg")})

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=ErrorResponse(
            error=ErrorDetail(
                code="VALIDATION_ERROR",
                message="Invalid query or path parameter.",
                details={"errors": simplified_errors},
            )
        ).model_dump(),
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    """Unhandled internal server exception fallback handler."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponse(
            error=ErrorDetail(
                code="INTERNAL_SERVER_ERROR",
                message="An unexpected internal server error occurred.",
            )
        ).model_dump(),
    )


# Include Routers
app.include_router(health_router)
app.include_router(watches_router)
app.include_router(collections_router)
app.include_router(search_router)
app.include_router(statistics_router)
