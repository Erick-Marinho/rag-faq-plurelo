import logging
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uvicorn
load_dotenv()
from app.services.rag_pipeline import faq_pipeline_instance


# Configura o logging para o projeto
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="RAG FAQ Plurelo",
    description="API para responder perguntas sobre a Plurelo usando RAG.",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Modelos Pydantic para a API ---
class AskRequest(BaseModel):
    question: str


class DocumentResponse(BaseModel):
    id: str
    content: str
    question: Optional[str] = None
    answer: Optional[str] = None
    source: Optional[str] = None
    score: Optional[float] = None


class AskResponse(BaseModel):
    answer: str
    documents: list[DocumentResponse]


# --- Endpoints da API ---
@app.get("/", summary="Mensagem de status da API", tags=["Status"])
async def root():
    return {
        "status": "success",
        "message": "API is running",
        "version": "0.1.0",
    }


@app.get("/health", summary="Verifica a saúde da API", tags=["Status"])
async def health():
    return {
        "status": "success",
        "message": "Health check successful",
        "version": "0.1.0",
    }


@app.post(
    "/faq/ask",
    summary="Pergunta ao FAQ",
    response_description="Resposta gerada e documentos recuperados",
    response_model=AskResponse,
    tags=["FAQ"],
)
async def ask(request: AskRequest):
    """
    Recebe uma pergunta e retorna uma resposta gerada por um pipeline de RAG,
    juntamente com os documentos de origem utilizados para a resposta.
    """
    logger.info(f"Recebida a pergunta: {request.question}")
    result = faq_pipeline_instance.ask(request.question)
    return result


if __name__ == "__main__":
    # Para executar: `uvicorn app.main:app --reload` a partir da raiz do projeto.
    uvicorn.run(app, host="0.0.0.0", port=8000)
