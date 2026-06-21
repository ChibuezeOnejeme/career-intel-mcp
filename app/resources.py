from __future__ import annotations

from fastmcp import FastMCP

STATIC_GUIDES = {
    "career://resume-guide": """# Resume Writing Guide

## Key Principles
- **Tailor each resume** to the specific role you're applying for
- **Quantify achievements** with numbers, percentages, and impact
- **Use action verbs** (led, built, optimized, delivered)
- **Keep it to one page** if you have less than 10 years experience

## Section Structure
1. **Header**: Name, email, phone, LinkedIn, portfolio
2. **Professional Summary**: 2-3 sentences highlighting your value proposition
3. **Skills**: Technical and soft skills, grouped by category
4. **Experience**: Reverse chronological, bullet points with STAR format
5. **Education**: Degree, institution, year, relevant coursework
6. **Certifications**: Relevant certifications with issuing body""",

    "career://interview-guide": """# Interview Preparation Guide

## Before the Interview
- Research the company, product, and culture
- Review the job description and prepare specific examples
- Practice the STAR method (Situation, Task, Action, Result)
- Prepare 3-5 questions to ask the interviewer

## During the Interview
- Listen carefully before answering
- Structure your answers (STAR method)
- Be honest about what you don't know
- Show enthusiasm and curiosity

## Common Question Types
1. **Behavioral**: "Tell me about a time when..."
2. **Technical**: Role-specific technical challenges
3. **Situational**: "What would you do if..."
4. **Cultural**: "What's your ideal work environment?" """,

    "career://salary-guide": """# Salary Negotiation Guide

## Before Negotiation
- Research market rates (Glassdoor, Levels.fyi, Blind)
- Know your minimum acceptable number
- Consider total compensation (base, bonus, equity, benefits)

## Negotiation Tactics
- Let the employer state the first number
- Always negotiate, even if the offer is good
- Focus on value you bring, not your needs
- Ask about growth path and review cycles""",

    "career://job-search-guide": """# Job Search Strategy Guide

## Phases
1. **Preparation**: Update resume, LinkedIn, portfolio
2. **Targeting**: Identify target companies and roles
3. **Networking**: Reach out to connections, attend events
4. **Applying**: Tailor each application
5. **Interviewing**: Prepare for each stage
6. **Evaluating**: Compare offers holistically""",

    "career://linkedin-guide": """# LinkedIn Optimization Guide

## Profile Sections
- **Headline**: Beyond your job title - include your value prop
- **About**: Story-driven summary with keywords
- **Experience**: Detailed with metrics
- **Skills**: Get endorsements, list 50+
- **Recommendations**: Request from managers and peers""",

    "career://career-roadmap-guide": """# Career Roadmap Guide

- Assess your current position and desired direction
- Identify skill gaps and create a learning plan
- Seek mentorship and sponsorship
- Build your personal brand
- Set 6-month, 1-year, and 3-year goals
- Regularly review and adjust your roadmap""",
}


def _make_static_resource(mcp: FastMCP, uri: str, content: str) -> None:
    @mcp.resource(uri)
    def _static_guide() -> str:
        return content


def register_resources(mcp: FastMCP) -> None:
    for uri, content in STATIC_GUIDES.items():
        _make_static_resource(mcp, uri, content)
