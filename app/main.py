from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.config import settings
from app.database import check_db, init_db
from app.llm import LLMProvider
from app.logging import get_logger, setup_logging
from app.prompts import register_prompts
from app.resources import register_resources
from app.scraper import JobScraperService
from app.services import (
    CandidateService,
    MarketService,
    ResumeService,
)

logger = get_logger(__name__)

llm_provider: LLMProvider | None = None
resume_svc: ResumeService | None = None
candidate_svc: CandidateService | None = None
scraper_svc: JobScraperService | None = None
market_svc: MarketService | None = None


@asynccontextmanager
async def lifespan(app: FastMCP) -> AsyncIterator[None]:
    global llm_provider, resume_svc, candidate_svc, scraper_svc, market_svc

    setup_logging(settings.log_level)
    logger.info("Starting Career Intelligence MCP...")

    await init_db()

    llm_provider = LLMProvider()
    resume_svc = ResumeService(llm=llm_provider)
    candidate_svc = CandidateService(llm=llm_provider)
    scraper_svc = JobScraperService()
    market_svc = MarketService(llm=llm_provider)

    from app.tools import register_tools

    register_tools(
        app,
        resume_svc=resume_svc,
        candidate_svc=candidate_svc,
        scraper_svc=scraper_svc,
        market_svc=market_svc,
        llm=llm_provider,
    )

    register_resources(app)
    register_prompts(app)

    logger.info("Career Intelligence MCP ready")
    yield

    if llm_provider:
        await llm_provider.close()
    if scraper_svc:
        await scraper_svc.close()
    logger.info("Career Intelligence MCP shut down")


mcp = FastMCP(
    "Career Intelligence MCP",
    instructions="AI-powered career intelligence platform for job seekers. Parse resumes, scrape and score job listings, analyze skill gaps, and prepare for interviews.",
    version="0.1.0",
    lifespan=lifespan,
)


@mcp.custom_route("/health", methods=["GET"])
async def health_check(request: Request) -> JSONResponse:
    db_ok = await check_db()
    llm_ok = llm_provider is not None
    return JSONResponse(
        {
            "status": "ok" if db_ok else "degraded",
            "database": "connected" if db_ok else "disconnected",
            "llm": "configured" if llm_ok else "not configured",
        }
    )


if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8000)
