import json
import logging
from pathlib import Path
from haystack import Pipeline
from haystack.components.embedders import (
    SentenceTransformersTextEmbedder,
    SentenceTransformersDocumentEmbedder,
)
from haystack.components.builders import AnswerBuilder, PromptBuilder
from haystack.components.generators import OpenAIGenerator
from haystack.document_stores.in_memory import InMemoryDocumentStore
from haystack.components.retrievers.in_memory import InMemoryEmbeddingRetriever
from haystack.dataclasses import Document
from haystack.components.preprocessors import DocumentSplitter
from haystack.components.writers import DocumentWriter
from haystack.utils import Secret

logger = logging.getLogger(__name__)

MODEL = "sentence-transformers/all-MiniLM-L6-v2"
FAQ_JSON_PATH = Path(__file__).parent.parent.parent / "faq_plurelo.json"


def load_docs(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        items = json.load(f)
    docs = []
    for i, it in enumerate(items):
        q = it["question"].strip()
        a = it["answer"].strip()
        content = f"Pergunta: {q}\nResposta: {a}"
        docs.append(
            Document(
                id=f"faq-{i+1}",
                content=content,
                meta={"question": q, "answer": a, "source": "faq_plurelo"},
            )
        )
    return docs


def build_document_store() -> InMemoryDocumentStore:
    logger.info("Inicializando o DocumentStore...")
    store = InMemoryDocumentStore()
    docs = load_docs(FAQ_JSON_PATH)

    splitter = DocumentSplitter(split_by="word", split_length=300, split_overlap=40)
    embedder = SentenceTransformersDocumentEmbedder(model=MODEL)
    embedder.warm_up()

    indexing_pipeline = Pipeline()
    indexing_pipeline.add_component("splitter", splitter)
    indexing_pipeline.add_component("embedder", embedder)
    indexing_pipeline.add_component("writer", DocumentWriter(document_store=store))

    indexing_pipeline.connect("splitter.documents", "embedder.documents")
    indexing_pipeline.connect("embedder.documents", "writer.documents")

    indexing_pipeline.run({"splitter": {"documents": docs}})

    logger.info(f"Indexados {store.count_documents()} documentos.")
    return store


class FaqPipeline:
    def __init__(self, document_store: InMemoryDocumentStore):
        self.document_store = document_store
        self.pipeline = self._build_pipeline()

    def _build_pipeline(self) -> Pipeline:
        logger.info("Construindo o pipeline de consulta RAG...")

        text_embedder = SentenceTransformersTextEmbedder(model=MODEL)
        retriever = InMemoryEmbeddingRetriever(
            document_store=self.document_store, top_k=3
        )

        template = """
        Com base no contexto fornecido, responda à pergunta de forma clara e concisa.
        Se a resposta não estiver no contexto, informe que você não possui a informação.

        Contexto:
        {% for doc in documents %}
            {{ doc.content }}
        {% endfor %}

        Pergunta: {{ query }}
        Resposta:
        """
        prompt_builder = PromptBuilder(template=template)

        generator = OpenAIGenerator(
            model="gpt-3.5-turbo", api_key=Secret.from_env_var("OPENAI_API_KEY")
        )

        answer_builder = AnswerBuilder()

        query_pipeline = Pipeline()
        query_pipeline.add_component("text_embedder", text_embedder)
        query_pipeline.add_component("retriever", retriever)
        query_pipeline.add_component("prompt_builder", prompt_builder)
        query_pipeline.add_component("llm_generator", generator)
        query_pipeline.add_component("answer_builder", answer_builder)

        query_pipeline.connect("text_embedder.embedding", "retriever.query_embedding")
        query_pipeline.connect("retriever.documents", "prompt_builder.documents")
        query_pipeline.connect("prompt_builder.prompt", "llm_generator.prompt")
        query_pipeline.connect("llm_generator.replies", "answer_builder.replies")
        query_pipeline.connect("retriever.documents", "answer_builder.documents")

        logger.info("Pipeline de consulta RAG construído com sucesso.")
        return query_pipeline

    def ask(self, question: str) -> dict:
        input_data = {
            "text_embedder": {"text": question},
            "prompt_builder": {"query": question},
            "answer_builder": {"query": question},
        }

        result = self.pipeline.run(input_data)
        answer_obj = result["answer_builder"]["answers"][0]

        return {
            "answer": answer_obj.data,
            "documents": [doc.to_dict() for doc in answer_obj.documents],
        }


document_store = build_document_store()
faq_pipeline_instance = FaqPipeline(document_store)
