from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from .routers import summarize
from .services.summarize import setup_qwen_client
from .config import get_settings
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Web Summarizer API", version="0.1.0")

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(summarize.router, prefix="/api")

# Initialize Qwen client on startup
@app.on_event("startup")
async def startup_event():
    try:
        settings = get_settings()
        if not settings.dashscope_api_key:
            logger.warning("DASHSCOPE_API_KEY is not set. Summarization may not work.")
        else:
            setup_qwen_client(settings.dashscope_api_key)
            logger.info("Qwen client initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize Qwen client: {str(e)}")
        # Don't raise here to allow the app to start without Qwen

# Health check endpoint
@app.get("/health")
async def health_check():
    settings = get_settings()
    return {
        "status": "healthy",
        "version": "0.1.0",
        "qwen_configured": bool(settings.dashscope_api_key)
    }

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error"},
    )
