from typing import Any

from pydantic import BaseModel, Field


class Experience(BaseModel):
    title: str
    company: str
    start_date: str | None = None
    end_date: str | None = None
    description: str | None = None
    bullet_points: list[str] = Field(default_factory=list)


class Education(BaseModel):
    degree: str
    institution: str
    year: int | None = None
    gpa: str | None = None


class ResumeData(BaseModel):
    name: str
    email: str
    phone: str | None = None
    location: str | None = None
    skills: list[str] = Field(default_factory=list)
    experience: list[Experience] = Field(default_factory=list)
    education: list[Education] = Field(default_factory=list)
    certifications: list[str] = Field(default_factory=list)
    summary: str | None = None


class ImproveResult(BaseModel):
    summary: str
    bullet_points: list[str] = Field(default_factory=list)
    suggested_skills: list[str] = Field(default_factory=list)


class MissingSkill(BaseModel):
    skill: str
    importance: str
    resources: list[str] = Field(default_factory=list)


class RoadmapItem(BaseModel):
    skill: str
    resources: list[str] = Field(default_factory=list)
    timeline: str
    priority: str


class SkillGapResult(BaseModel):
    current_skills: list[str] = Field(default_factory=list)
    missing_skills: list[MissingSkill] = Field(default_factory=list)
    roadmap: list[RoadmapItem] = Field(default_factory=list)


class CareerPathResult(BaseModel):
    next_role: str
    skills_needed: list[str] = Field(default_factory=list)
    certifications: list[str] = Field(default_factory=list)
    timeline_months: int = 12


class SalaryEstimate(BaseModel):
    min: float
    max: float
    currency: str = "USD"
    confidence: str = "medium"
    factors: list[str] = Field(default_factory=list)


class JobListing(BaseModel):
    title: str
    company: str
    location: str | None = None
    description: str
    url: str | None = None
    salary_min: float | None = None
    salary_max: float | None = None
    currency: str = "USD"
    posted_days_ago: int | None = None
    source: str | None = None


class JobSearchResult(BaseModel):
    query: str
    location: str | None = None
    jobs: list[JobListing] = Field(default_factory=list)
    total_found: int = 0
    sources_used: list[str] = Field(default_factory=list)


class ScoredJob(BaseModel):
    job: JobListing
    score: float
    match_reasons: list[str] = Field(default_factory=list)
    weaknesses: list[str] = Field(default_factory=list)


class ScoreJobsResult(BaseModel):
    scored_jobs: list[ScoredJob] = Field(default_factory=list)
    summary: str | None = None


class CompareResult(BaseModel):
    strengths: dict[str, list[str]] = Field(default_factory=dict)
    risks: dict[str, list[str]] = Field(default_factory=dict)
    salary_comparison: dict[str, dict[str, float | None]] = Field(default_factory=dict)
    skill_overlap: list[str] = Field(default_factory=list)
    overall_recommendation: str | None = None


class InterviewQuestions(BaseModel):
    technical: list[str] = Field(default_factory=list)
    behavioral: list[str] = Field(default_factory=list)
    follow_up: list[str] = Field(default_factory=list)


class MarketAnalysis(BaseModel):
    trend: str
    demand_skills: list[str] = Field(default_factory=list)
    salary_range: dict[str, Any] = Field(default_factory=dict)
    insights: list[str] = Field(default_factory=list)
