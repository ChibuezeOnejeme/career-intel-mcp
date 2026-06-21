from __future__ import annotations

from fastmcp import FastMCP

from app.schemas import (
    CareerPathResult,
    CompareResult,
    ImproveResult,
    InterviewQuestions,
    JobListing,
    MarketAnalysis,
    ResumeData,
    SalaryEstimate,
    ScoreJobsResult,
    SkillGapResult,
)
from app.scraper import JobScraperService
from app.services import (
    CandidateService,
    MarketService,
    ResumeService,
    generate_interview_questions_for_role,
)
from app.services import (
    compare_jobs as _compare_jobs,
)
from app.services import (
    score_jobs_for_candidate as _score_jobs_for_candidate,
)


def register_tools(
    mcp: FastMCP,
    resume_svc: ResumeService,
    candidate_svc: CandidateService,
    scraper_svc: JobScraperService,
    market_svc: MarketService,
    llm,  # noqa: ANN001
) -> None:
    @mcp.tool()
    async def parse_resume(raw_text: str, email: str | None = None) -> ResumeData:
        """Parse a raw resume text and extract structured information including name, skills, experience, education, and certifications. Paste your full resume text."""
        return await resume_svc.parse_resume(raw_text, email)

    @mcp.tool()
    async def improve_resume(
        resume_text: str, target_role: str | None = None
    ) -> ImproveResult:
        """Improve a resume with a better professional summary, stronger bullet points, and suggested skills. Optionally specify a target role to tailor the improvements."""
        return await resume_svc.improve_resume(resume_text, target_role)

    @mcp.tool()
    async def scrape_job_listing(url: str) -> JobListing:
        """Scrape a job listing from a URL. Supports LinkedIn, Indeed, Glassdoor, WeWorkRemotely, RemoteOK, and any generic webpage. Paste the full URL of the job posting."""
        return await scraper_svc.scrape_job_listing(url)

    @mcp.tool()
    async def score_jobs_for_candidate(
        resume_text: str, jobs: list[JobListing]
    ) -> ScoreJobsResult:
        """Score a list of jobs against a resume. Returns a 0-100 match score per job, match reasons, and weaknesses. Use after scraping job listings."""
        return await _score_jobs_for_candidate(llm, resume_text, jobs)

    @mcp.tool()
    async def compare_jobs(jobs: list[JobListing]) -> CompareResult:
        """Compare 2 or more job listings side-by-side. Returns strengths, risks, salary comparison, skill overlap, and an overall recommendation."""
        return await _compare_jobs(llm, jobs)

    @mcp.tool()
    async def skill_gap_analysis(resume_text: str, target_role: str) -> SkillGapResult:
        """Analyze skill gaps between a resume and a target role. Returns missing skills with importance levels, learning resources, and a prioritized roadmap."""
        return await candidate_svc.skill_gap_analysis(resume_text, target_role)

    @mcp.tool()
    async def career_path(resume_text: str) -> CareerPathResult:
        """Generate a career progression path from a resume. Returns the next likely role, skills to develop, recommended certifications, and a timeline."""
        return await candidate_svc.career_path(resume_text)

    @mcp.tool()
    async def salary_estimate(
        skills: list[str], experience_years: int, location: str
    ) -> SalaryEstimate:
        """Estimate a salary range based on skills, years of experience, and location. Returns min/max salary, confidence level, and the key factors influencing the range."""
        return await candidate_svc.salary_estimate(skills, experience_years, location)

    @mcp.tool()
    async def generate_interview_questions(
        job_description: str, candidate_resume: str | None = None
    ) -> InterviewQuestions:
        """Generate interview questions for a job description. Includes technical, behavioral, and follow-up questions. Optionally provide a candidate resume to personalize."""
        return await generate_interview_questions_for_role(llm, job_description, candidate_resume)

    @mcp.tool()
    async def job_market_analysis(
        industry: str, location: str | None = None
    ) -> MarketAnalysis:
        """Analyze current hiring trends for an industry and location. Returns demand skills, salary ranges, and market insights."""
        return await market_svc.job_market_analysis(industry, location)

    @mcp.tool()
    async def skill_demand_analysis(skills: list[str]) -> dict:
        """Analyze the market demand for a list of skills. Returns demand level (high/medium/low), growth trend, and market insights for each skill."""
        return await market_svc.skill_demand_analysis(skills)
