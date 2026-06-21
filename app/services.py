import json
from typing import Any

from app.llm import LLMProvider
from app.logging import get_logger
from app.schemas import (
    CareerPathResult,
    CompareResult,
    ImproveResult,
    InterviewQuestions,
    JobListing,
    MarketAnalysis,
    ResumeData,
    SalaryEstimate,
    ScoredJob,
    ScoreJobsResult,
    SkillGapResult,
)

logger = get_logger(__name__)

SYSTEM_PROMPTS = {
    "parse_resume": "You are a resume parser. Extract structured information from the resume text. Return ONLY valid JSON.",
    "improve_resume": "You are a professional resume writer. Improve the given resume for the target role. Return ONLY valid JSON.",
    "skill_gap": "You are a career development expert. Analyze skill gaps and create a learning roadmap. Return ONLY valid JSON.",
    "career_path": "You are a career strategist. Design a career progression path. Return ONLY valid JSON.",
    "salary_estimate": "You are a compensation analyst. Estimate salary ranges based on skills, experience, and location. Return ONLY valid JSON.",
    "score_jobs": "You are a talent acquisition expert. Score each job against the resume and explain the match. Return ONLY valid JSON.",
    "compare_jobs": "You are a job market analyst. Compare multiple job opportunities. Return ONLY valid JSON.",
    "interview_questions": "You are a technical interviewer. Generate interview questions. Return ONLY valid JSON.",
    "market_analysis": "You are a labor market economist. Analyze hiring trends. Return ONLY valid JSON.",
    "skill_demand": "You are a workforce analyst. Identify high-demand skills. Return ONLY valid JSON.",
    "salary_trends": "You are a compensation analyst. Analyze salary trends. Return ONLY valid JSON.",
}


class ResumeService:
    def __init__(self, llm: LLMProvider) -> None:
        self.llm = llm

    async def parse_resume(self, raw_text: str, email: str | None = None) -> ResumeData:
        content = await self.llm.generate(
            prompt=f"Parse this resume and extract name, email, phone, location, skills, experience, education, certifications, and a brief summary:\n\n{raw_text}",
            system=SYSTEM_PROMPTS["parse_resume"],
            json_mode=True,
        )
        data = json.loads(content)
        parsed = ResumeData(**data)

        from app.database import async_session_factory
        from app.models import Candidate
        from app.repository import CandidateRepository

        async with async_session_factory() as session:
            repo = CandidateRepository(session)
            candidate = Candidate(
                name=parsed.name,
                email=email or parsed.email,
                phone=parsed.phone,
                location=parsed.location,
                skills=parsed.skills,
                experience=[e.model_dump() for e in parsed.experience],
                education=[e.model_dump() for e in parsed.education],
                certifications=parsed.certifications,
                summary=parsed.summary,
                parsed_resume_raw=raw_text,
            )
            await repo.create(candidate)

        return parsed

    async def improve_resume(
        self, resume_text: str, target_role: str | None = None
    ) -> ImproveResult:
        prompt = f"Improve this resume. Generate a better professional summary, improved bullet points for each experience, and suggested skills to add:\n\n{resume_text}"
        if target_role:
            prompt = f"Improve this resume for a {target_role} role. Focus on relevant skills and experience. Generate a better professional summary, improved bullet points, and suggested skills:\n\n{resume_text}"

        content = await self.llm.generate(
            prompt=prompt,
            system=SYSTEM_PROMPTS["improve_resume"],
            json_mode=True,
        )
        result = json.loads(content)
        return ImproveResult(**result)


class CandidateService:
    def __init__(self, llm: LLMProvider) -> None:
        self.llm = llm

    async def skill_gap_analysis(
        self, resume_text: str, target_role: str
    ) -> SkillGapResult:
        content = await self.llm.generate(
            prompt=f"Analyze skill gaps for transitioning to '{target_role}'. Resume:\n{resume_text}\n\nProvide current_skills, missing_skills (skill, importance, resources), and a roadmap (skill, resources, timeline, priority).\n\nReturn ONLY valid JSON.",
            system=SYSTEM_PROMPTS["skill_gap"],
            json_mode=True,
        )
        result = json.loads(content)
        return SkillGapResult(**result)

    async def career_path(self, resume_text: str) -> CareerPathResult:
        content = await self.llm.generate(
            prompt=f"Design a career progression path based on this resume. Provide next_role, skills_needed, certifications, and timeline_months.\n\nResume:\n{resume_text}\n\nReturn ONLY valid JSON.",
            system=SYSTEM_PROMPTS["career_path"],
            json_mode=True,
        )
        result = json.loads(content)
        return CareerPathResult(**result)

    async def salary_estimate(
        self, skills: list[str], experience_years: int, location: str
    ) -> SalaryEstimate:
        content = await self.llm.generate(
            prompt=f"Estimate salary based on: Skills: {json.dumps(skills)}, Experience: {experience_years} years, Location: {location}. Provide min, max, currency, confidence (low/medium/high), and factors influencing the estimate.\n\nReturn ONLY valid JSON.",
            system=SYSTEM_PROMPTS["salary_estimate"],
            json_mode=True,
        )
        result = json.loads(content)
        return SalaryEstimate(**result)


class MarketService:
    def __init__(self, llm: LLMProvider) -> None:
        self.llm = llm

    async def job_market_analysis(
        self, industry: str, location: str | None = None
    ) -> MarketAnalysis:
        prompt = f"Analyze job market trends for {industry}"
        if location:
            prompt += f" in {location}"
        prompt += ". Provide trend (short description), demand_skills (list), salary_range (min, max, currency), and insights (list).\n\nReturn ONLY valid JSON."

        content = await self.llm.generate(
            prompt=prompt,
            system=SYSTEM_PROMPTS["market_analysis"],
            json_mode=True,
        )
        result = json.loads(content)
        return MarketAnalysis(**result)

    async def skill_demand_analysis(self, skills: list[str]) -> dict[str, Any]:
        content = await self.llm.generate(
            prompt=f"Analyze demand for these skills: {json.dumps(skills)}. For each skill, provide demand_level (high/medium/low), growth_trend (rising/stable/declining), and market_insights.\n\nReturn ONLY valid JSON.",
            system=SYSTEM_PROMPTS["skill_demand"],
            json_mode=True,
        )
        return json.loads(content)

    async def salary_trend_analysis(
        self, role: str, location: str | None = None
    ) -> dict[str, Any]:
        prompt = f"Analyze salary trends for {role}"
        if location:
            prompt += f" in {location}"
        prompt += ". Provide salary_range (min, max, currency), year_over_year_change (percentage), factors affecting salary, and outlook.\n\nReturn ONLY valid JSON."

        content = await self.llm.generate(
            prompt=prompt,
            system=SYSTEM_PROMPTS["salary_trends"],
            json_mode=True,
        )
        return json.loads(content)


async def score_jobs_for_candidate(
    llm: LLMProvider, resume_text: str, jobs: list[JobListing]
) -> ScoreJobsResult:
    if not jobs:
        return ScoreJobsResult(scored_jobs=[], summary="No jobs to score.")

    jobs_json = json.dumps([j.model_dump() for j in jobs], indent=2, default=str)
    prompt = f"""Score each job against the resume below. For each job, give a score 0-100, match_reasons (why it's a good fit), and weaknesses (gaps or concerns).
Resume:
{resume_text}

Jobs:
{jobs_json}

Return ONLY valid JSON with a top-level "scored_jobs" array. Each entry should have: job (the full job object), score (0-100 float), match_reasons (list of strings), weaknesses (list of strings). Also include a "summary" key with an overall summary string."""

    content = await llm.generate(
        prompt=prompt,
        system=SYSTEM_PROMPTS["score_jobs"],
        json_mode=True,
    )
    result = json.loads(content)

    scored_jobs = [
        ScoredJob(
            job=JobListing(**sj["job"]) if isinstance(sj["job"], dict) else sj["job"],
            score=sj["score"],
            match_reasons=sj.get("match_reasons", []),
            weaknesses=sj.get("weaknesses", []),
        )
        for sj in result.get("scored_jobs", [])
    ]

    scored_jobs.sort(key=lambda x: x.score, reverse=True)

    return ScoreJobsResult(
        scored_jobs=scored_jobs,
        summary=result.get("summary"),
    )


async def compare_jobs(llm: LLMProvider, jobs: list[JobListing]) -> CompareResult:
    if len(jobs) < 2:
        raise ValueError("Need at least 2 jobs to compare")

    jobs_json = json.dumps([j.model_dump() for j in jobs], indent=2, default=str)
    prompt = f"""Compare the following job opportunities. For each, list strengths, risks, salary comparison, and skill overlap between all jobs. Also provide an overall_recommendation.
Jobs:
{jobs_json}

Return ONLY valid JSON with: strengths (dict of job title -> list of strings), risks (dict), salary_comparison (dict of job title -> {{min, max}}), skill_overlap (list), overall_recommendation (string)."""

    content = await llm.generate(
        prompt=prompt,
        system=SYSTEM_PROMPTS["compare_jobs"],
        json_mode=True,
    )
    result = json.loads(content)
    return CompareResult(**result)


async def generate_interview_questions_for_role(
    llm: LLMProvider,
    job_description: str,
    candidate_resume: str | None = None,
) -> InterviewQuestions:
    prompt = f"""Generate interview questions based on this job description.
Job Description:
{job_description}
"""
    if candidate_resume:
        prompt += f"\n\nCandidate Profile (for personalization):\n{candidate_resume}\n"

    prompt += "\n\nGenerate technical questions, behavioral questions, and follow-up questions. Return ONLY valid JSON with keys: technical, behavioral, follow_up."

    content = await llm.generate(
        prompt=prompt,
        system=SYSTEM_PROMPTS["interview_questions"],
        json_mode=True,
    )
    result = json.loads(content)
    return InterviewQuestions(**result)
