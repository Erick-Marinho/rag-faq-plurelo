import logging
from dotenv import load_dotenv
from dotenv.main import logger
from fastapi import FastAPI
import uvicorn


load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

app = FastAPI(
    title="RAG FAQ Plurelo",
    description="RAG FAQ Plurelo",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

@app.get("/", summary="Return a basic message", response_description="A basic message")
async def root():
    return {
        "status": "success",
        "message": "Plurelo API is running",
        "version": "0.1.0",
    }

@app.get("/health", summary="Check health of the API", response_description="Health check of the API")
async def health():
    return {
        "status": "success",
        "message": "Plurelo API is running",
        "version": "0.1.0",
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
