import pytest

from tests.conftest import MockLLM, MockScraper


@pytest.mark.asyncio
async def test_parse_resume_tool_calls_service(
    resume_service,
    sample_resume_text: str,
):
    result = await resume_service.parse_resume(sample_resume_text)
    assert result.name == "John Doe"
    assert result.email == "john@example.com"


@pytest.mark.asyncio
async def test_improve_resume_tool_calls_service(
    resume_service,
    sample_resume_text: str,
):
    result = await resume_service.improve_resume(sample_resume_text, "Staff Engineer")
    assert result.summary
    assert result.suggested_skills


@pytest.mark.asyncio
async def test_scrape_job_listing_linkedin(scraper_service: MockScraper):
    url = "https://www.linkedin.com/jobs/view/12345"
    result = await scraper_service.scrape_job_listing(url)
    assert result.source == "linkedin"
    assert result.title == "Senior Backend Engineer"


@pytest.mark.asyncio
async def test_scrape_job_listing_indeed(scraper_service: MockScraper):
    url = "https://www.indeed.com/jobs/view/67890"
    result = await scraper_service.scrape_job_listing(url)
    assert result.source == "indeed"
    assert result.company == "Indeed Inc"


@pytest.mark.asyncio
async def test_scrape_job_listing_generic(scraper_service: MockScraper):
    url = "https://www.randomjobsite.com/view/999"
    result = await scraper_service.scrape_job_listing(url)
    assert result.source == "generic"


@pytest.mark.asyncio
async def test_skill_gap_analysis_tool_calls_service(
    candidate_service,
    sample_resume_text: str,
):
    result = await candidate_service.skill_gap_analysis(
        sample_resume_text, "Staff Engineer"
    )
    assert result.current_skills
    assert result.roadmap


@pytest.mark.asyncio
async def test_career_path_tool_calls_service(
    candidate_service,
    sample_resume_text: str,
):
    result = await candidate_service.career_path(sample_resume_text)
    assert result.next_role
    assert result.timeline_months > 0


@pytest.mark.asyncio
async def test_salary_estimate_tool_calls_service(candidate_service):
    result = await candidate_service.salary_estimate(
        skills=["Python", "AWS"],
        experience_years=5,
        location="San Francisco",
    )
    assert result.min > 0
    assert result.max > result.min


@pytest.mark.asyncio
async def test_generate_interview_questions_tool(
    mock_llm: MockLLM,
):
    from app.services import generate_interview_questions_for_role

    result = await generate_interview_questions_for_role(
        mock_llm,
        job_description="Python backend engineer with AWS",
    )
    assert result.technical
    assert result.behavioral


@pytest.mark.asyncio
async def test_job_market_analysis_tool_calls_service(market_service):
    result = await market_service.job_market_analysis(
        industry="Software Engineering",
        location="San Francisco",
    )
    assert result.trend
    assert result.demand_skills


@pytest.mark.asyncio
async def test_skill_demand_analysis_tool_calls_service(market_service):
    result = await market_service.skill_demand_analysis(["Python", "Rust"])
    assert "Python" in result
