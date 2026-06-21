import json
from unittest.mock import MagicMock

import pytest
from fastmcp import FastMCP

from app.llm import LLMProvider
from app.scraper import JobScraperService
from app.services import (
    CandidateService,
    MarketService,
    ResumeService,
)


@pytest.fixture(autouse=True)
def setup_test_db():
    from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

    import app.database
    from app.models import Base

    engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=False)
    test_session_factory = async_sessionmaker(engine, expire_on_commit=False)

    import asyncio

    async def init_tables():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    asyncio.run(init_tables())

    original_factory = app.database.async_session_factory
    app.database.async_session_factory = test_session_factory

    yield

    app.database.async_session_factory = original_factory


class MockLLM(LLMProvider):
    def __init__(self) -> None:
        self.call_count = 0
        self.last_prompt = ""

    async def embed(self, text: str) -> list[float]:
        return [0.1] * 1536

    async def generate(
        self,
        prompt: str,
        system: str | None = None,
        json_mode: bool = False,
    ) -> str:
        self.call_count += 1
        self.last_prompt = prompt
        if "Parse this resume" in prompt:
            return json.dumps(
                {
                    "name": "John Doe",
                    "email": "john@example.com",
                    "phone": "555-0100",
                    "location": "San Francisco, CA",
                    "skills": ["Python", "FastAPI", "PostgreSQL"],
                    "experience": [
                        {
                            "title": "Senior Engineer",
                            "company": "Tech Co",
                            "start_date": "2020-01",
                            "end_date": "present",
                            "description": "Built APIs",
                            "bullet_points": ["Led team of 5", "Improved perf 40%"],
                        }
                    ],
                    "education": [
                        {
                            "degree": "BS Computer Science",
                            "institution": "MIT",
                            "year": 2015,
                        }
                    ],
                    "certifications": ["AWS Solutions Architect"],
                    "summary": "Experienced engineer",
                }
            )
        if "Improve this resume" in prompt:
            return json.dumps(
                {
                    "summary": "Senior engineer with 8+ years...",
                    "bullet_points": ["Orchestrated migration", "Reduced costs 30%"],
                    "suggested_skills": ["Kubernetes", "Terraform"],
                }
            )
        if "Analyze skill gaps" in prompt:
            return json.dumps(
                {
                    "current_skills": ["Python", "FastAPI"],
                    "missing_skills": [
                        {
                            "skill": "Kubernetes",
                            "importance": "high",
                            "resources": ["K8s docs"],
                        }
                    ],
                    "roadmap": [
                        {
                            "skill": "Kubernetes",
                            "resources": ["K8s documentation", "CKA course"],
                            "timeline": "3 months",
                            "priority": "high",
                        }
                    ],
                }
            )
        if "Design a career progression" in prompt:
            return json.dumps(
                {
                    "next_role": "Engineering Manager",
                    "skills_needed": ["People management", "Budget planning"],
                    "certifications": ["PMP", "Leadership certificate"],
                    "timeline_months": 18,
                }
            )
        if "Estimate salary" in prompt:
            return json.dumps(
                {
                    "min": 140000,
                    "max": 180000,
                    "currency": "USD",
                    "confidence": "high",
                    "factors": ["High demand skills", "SF Bay Area premium"],
                }
            )
        if "Score each job" in prompt:
            return json.dumps(
                {
                    "scored_jobs": [
                        {
                            "job": {
                                "title": "Senior Backend Engineer",
                                "company": "Tech Corp",
                                "location": "Remote",
                                "description": "Build scalable APIs",
                                "url": "https://example.com/job/1",
                                "salary_min": 150000,
                                "salary_max": 200000,
                                "currency": "USD",
                                "posted_days_ago": 3,
                                "source": "linkedin",
                            },
                            "score": 85.0,
                            "match_reasons": ["Strong Python", "Remote OK"],
                            "weaknesses": ["Leadership not explicit"],
                        }
                    ],
                    "summary": "Overall strong match.",
                }
            )
        if "Compare the following job" in prompt:
            return json.dumps(
                {
                    "strengths": {
                        "Job A": ["Higher salary", "Remote option"],
                        "Job B": ["Better benefits", "Growth opportunity"],
                    },
                    "risks": {
                        "Job A": ["Startup instability"],
                        "Job B": ["Long commute"],
                    },
                    "salary_comparison": {
                        "Job A": {"min": 150000, "max": 200000},
                        "Job B": {"min": 130000, "max": 170000},
                    },
                    "skill_overlap": ["Python", "PostgreSQL", "AWS"],
                    "overall_recommendation": "Job A if salary-driven, Job B if growth-driven.",
                }
            )
        if "Generate interview questions" in prompt:
            return json.dumps(
                {
                    "technical": ["Explain Python async/await", "Design a rate limiter"],
                    "behavioral": ["Tell me about a conflict", "Describe a failure"],
                    "follow_up": ["How would you scale this?", "What about edge cases?"],
                }
            )
        if "Analyze job market trends" in prompt:
            return json.dumps(
                {
                    "trend": "Growing demand for AI/ML engineers",
                    "demand_skills": ["Machine Learning", "Python", "PyTorch"],
                    "salary_range": {"min": 120000, "max": 250000, "currency": "USD"},
                    "insights": ["Remote roles increasing 40% YoY"],
                }
            )
        if "Analyze demand for these skills" in prompt:
            return json.dumps(
                {
                    "Python": {
                        "demand_level": "high",
                        "growth_trend": "rising",
                        "market_insights": "Core skill for AI, data, and backend roles",
                    }
                }
            )
        if "Analyze salary trends" in prompt:
            return json.dumps(
                {
                    "salary_range": {"min": 130000, "max": 200000},
                    "year_over_year_change": 8.5,
                    "factors": ["AI talent scarcity", "Remote competition"],
                    "outlook": "Continued growth expected",
                }
            )
        return json.dumps({"result": "ok"})


@pytest.fixture
def mock_llm() -> MockLLM:
    return MockLLM()


class MockScraper(JobScraperService):
    def __init__(self) -> None:
        pass

    async def scrape_job_listing(self, url: str):
        if "linkedin" in url:
            return MagicMock(
                title="Senior Backend Engineer",
                company="Tech Corp",
                location="San Francisco, CA",
                description="Build scalable APIs with Python. 5+ years experience required.",
                url=url,
                salary_min=150000.0,
                salary_max=200000.0,
                currency="USD",
                posted_days_ago=3,
                source="linkedin",
            )
        elif "indeed" in url:
            return MagicMock(
                title="Backend Engineer",
                company="Indeed Inc",
                location="Remote",
                description="Fast-paced backend development with Python and PostgreSQL.",
                url=url,
                salary_min=130000.0,
                salary_max=170000.0,
                currency="USD",
                posted_days_ago=5,
                source="indeed",
            )
        else:
            return MagicMock(
                title="Software Engineer",
                company="Example Corp",
                location="New York, NY",
                description="Full-stack development role.",
                url=url,
                salary_min=None,
                salary_max=None,
                currency="USD",
                posted_days_ago=None,
                source="generic",
            )

    async def close(self) -> None:
        pass


@pytest.fixture
def scraper_service() -> MockScraper:
    return MockScraper()


@pytest.fixture
def resume_service(mock_llm: MockLLM) -> ResumeService:
    return ResumeService(llm=mock_llm)


@pytest.fixture
def candidate_service(mock_llm: MockLLM) -> CandidateService:
    return CandidateService(llm=mock_llm)


@pytest.fixture
def market_service(mock_llm: MockLLM) -> MarketService:
    return MarketService(llm=mock_llm)


@pytest.fixture
def mock_mcp(
    resume_service: ResumeService,
    candidate_service: CandidateService,
    scraper_service: MockScraper,
    market_service: MarketService,
    mock_llm: MockLLM,
) -> FastMCP:
    mcp = FastMCP("test-mcp")
    from app.tools import register_tools

    register_tools(
        mcp,
        resume_svc=resume_service,
        candidate_svc=candidate_service,
        scraper_svc=scraper_service,
        market_svc=market_service,
        llm=mock_llm,
    )
    return mcp


@pytest.fixture
def sample_resume_text() -> str:
    return """John Doe
john@example.com | 555-0100
San Francisco, CA

Senior Software Engineer with 8+ years of experience building scalable APIs.

Skills: Python, FastAPI, PostgreSQL, AWS, Docker

Experience:
Senior Engineer, Tech Co (2020-present)
- Led team of 5 engineers
- Improved API performance by 40%
- Designed microservices architecture

Education:
BS Computer Science, MIT (2015)

Certifications: AWS Solutions Architect"""
