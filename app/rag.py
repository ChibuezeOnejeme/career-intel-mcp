from dataclasses import dataclass
from typing import Any

from app.database import async_session_factory
from app.llm import LLMProvider
from app.logging import get_logger
from app.models import Embedding
from app.repository import EmbeddingRepository

logger = get_logger(__name__)


@dataclass
class SearchResult:
    source_id: str
    source_type: str
    content: str
    metadata: dict[str, Any]
    score: float


class RAGService:
    def __init__(self, llm: LLMProvider) -> None:
        self.llm = llm

    async def generate_embedding(self, text: str) -> list[float]:
        return await self.llm.embed(text)

    async def embed_document(
        self,
        source_type: str,
        source_id: str,
        content: str,
        metadata: dict[str, Any] | None = None,
    ) -> Embedding:
        embedding_vector = await self.generate_embedding(content)
        async with async_session_factory() as session:
            repo = EmbeddingRepository(session)
            emb = Embedding(
                source_type=source_type,
                source_id=source_id,
                content=content,
                embedding=embedding_vector,
                extra_meta=metadata or {},
            )
            return await repo.store(emb)

    async def semantic_search(
        self,
        query: str,
        source_type: str | None = None,
        limit: int = 10,
        threshold: float = 0.7,
    ) -> list[SearchResult]:
        query_embedding = await self.generate_embedding(query)
        async with async_session_factory() as session:
            repo = EmbeddingRepository(session)
            results = await repo.semantic_search(
                query_embedding, source_type, limit, threshold
            )
            search_results: list[SearchResult] = []
            for emb in results:
                search_results.append(
                    SearchResult(
                        source_id=emb.source_id,
                        source_type=emb.source_type,
                        content=emb.content,
                        metadata=emb.extra_meta or {},
                        score=1.0,
                    )
                )
            return search_results

    async def retrieve_context(
        self,
        query: str,
        source_types: list[str] | None = None,
        limit: int = 5,
    ) -> str:
        results = await self.semantic_search(query, limit=limit)
        if source_types:
            results = [r for r in results if r.source_type in source_types]

        if not results:
            return ""

        context_parts = []
        for i, r in enumerate(results, 1):
            context_parts.append(
                f"[{i}] Source: {r.source_type}\nContent: {r.content}\n"
            )
        return "\n---\n".join(context_parts)
