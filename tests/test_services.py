import pytest

from tests.conftest import MockLLM


@pytest.mark.asyncio
async def test_parse_resume_returns_structured_data(
    resume_service,
    sample_resume_text: str,
    mock_llm: MockLLM,
):
    result = await resume_service.parse_resume(sample_resume_text)
    assert result.name == "John Doe"
    assert result.email == "john@example.com"
    assert "Python" in result.skills
    assert "MIT" in [e.institution for e in result.education]


@pytest.mark.asyncio
async def test_parse_resume_calls_llm(
    resume_service,
    sample_resume_text: str,
    mock_llm: MockLLM,
):
    await resume_service.parse_resume(sample_resume_text)
    assert mock_llm.call_count >= 1
    assert "Parse this resume" in mock_llm.last_prompt


@pytest.mark.asyncio
async def test_improve_resume_returns_improved_content(
    resume_service,
    sample_resume_text: str,
    mock_llm: MockLLM,
):
    result = await resume_service.improve_resume(sample_resume_text)
    assert result.summary
    assert result.suggested_skills


@pytest.mark.asyncio
async def test_improve_resume_with_target_role(
    resume_service,
    sample_resume_text: str,
):
    result = await resume_service.improve_resume(sample_resume_text, target_role="Staff Engineer")
    assert result.summary


@pytest.mark.asyncio
async def test_skill_gap_analysis(
    candidate_service,
    sample_resume_text: str,
    mock_llm: MockLLM,
):
    result = await candidate_service.skill_gap_analysis(sample_resume_text, "Staff Engineer")
    assert result.current_skills
    assert result.roadmap


@pytest.mark.asyncio
async def test_career_path(
    candidate_service,
    sample_resume_text: str,
    mock_llm: MockLLM,
):
    result = await candidate_service.career_path(sample_resume_text)
    assert result.next_role
    assert result.timeline_months > 0


@pytest.mark.asyncio
async def test_salary_estimate(candidate_service, mock_llm: MockLLM):
    result = await candidate_service.salary_estimate(
        skills=["Python", "AWS", "PostgreSQL"],
        experience_years=5,
        location="San Francisco, CA",
    )
    assert result.min > 0
    assert result.max > result.min
    assert result.currency == "USD"


@pytest.mark.asyncio
async def test_job_market_analysis(market_service, mock_llm: MockLLM):
    result = await market_service.job_market_analysis("Software Engineering", "San Francisco")
    assert result.trend
    assert result.demand_skills


@pytest.mark.asyncio
async def test_skill_demand_analysis(market_service, mock_llm: MockLLM):
    result = await market_service.skill_demand_analysis(["Python", "Rust"])
    assert "Python" in result


@pytest.mark.asyncio
async def test_salary_trend_analysis(market_service, mock_llm: MockLLM):
    result = await market_service.salary_trend_analysis("Backend Engineer", "Remote")
    assert "salary_range" in result


@pytest.mark.asyncio
async def test_score_jobs_for_candidate_filters_by_score(
    sample_resume_text: str,
    mock_llm: MockLLM,
):
    from app.schemas import JobListing
    from app.services import score_jobs_for_candidate

    jobs = [
        JobListing(
            title="Senior Backend Engineer",
            company="Tech Corp",
            location="Remote",
            description="Build APIs with Python",
            url="https://example.com/1",
            salary_min=150000,
            salary_max=200000,
            currency="USD",
            source="linkedin",
        )
    ]

    result = await score_jobs_for_candidate(mock_llm, sample_resume_text, jobs)
    assert len(result.scored_jobs) == 1
    assert result.scored_jobs[0].score > 0


@pytest.mark.asyncio
async def test_score_jobs_for_candidate_empty_list_returns_empty(
    sample_resume_text: str,
    mock_llm: MockLLM,
):
    from app.services import score_jobs_for_candidate

    result = await score_jobs_for_candidate(mock_llm, sample_resume_text, [])
    assert result.scored_jobs == []
    assert "No jobs" in result.summary


@pytest.mark.asyncio
async def test_compare_jobs_requires_at_least_two(
    mock_llm: MockLLM,
):
    from app.schemas import JobListing
    from app.services import compare_jobs

    with pytest.raises(ValueError, match="at least 2"):
        await compare_jobs(
            mock_llm,
            [
                JobListing(
                    title="Job A",
                    company="Corp A",
                    description="Desc",
                    url="https://a.com",
                )
            ],
        )


@pytest.mark.asyncio
async def test_compare_jobs_returns_comparison(
    mock_llm: MockLLM,
):
    from app.schemas import JobListing
    from app.services import compare_jobs

    jobs = [
        JobListing(
            title="Job A",
            company="Corp A",
            description="Python, remote",
            url="https://a.com",
            salary_min=150000,
            salary_max=200000,
            currency="USD",
            source="linkedin",
        ),
        JobListing(
            title="Job B",
            company="Corp B",
            description="Java, hybrid",
            url="https://b.com",
            salary_min=130000,
            salary_max=170000,
            currency="USD",
            source="indeed",
        ),
    ]

    result = await compare_jobs(mock_llm, jobs)
    assert result.overall_recommendation
    assert len(result.skill_overlap) >= 0


@pytest.mark.asyncio
async def test_generate_interview_questions_returns_structured(
    mock_llm: MockLLM,
):
    from app.services import generate_interview_questions_for_role

    result = await generate_interview_questions_for_role(
        mock_llm,
        job_description="Python backend engineer with AWS experience needed",
    )
    assert result.technical
    assert result.behavioral
    assert result.follow_up


@pytest.mark.asyncio
async def test_generate_interview_questions_with_resume(
    mock_llm: MockLLM,
    sample_resume_text: str,
):
    from app.services import generate_interview_questions_for_role

    result = await generate_interview_questions_for_role(
        mock_llm,
        job_description="Python backend engineer with AWS",
        candidate_resume=sample_resume_text,
    )
    assert result.technical
