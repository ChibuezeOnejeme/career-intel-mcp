# Career Intelligence MCP - Complete Prompt Guide

A comprehensive guide for using the Career Intelligence MCP server with Claude. This MCP provides 12 career-focused tools powered by LLMs.

---

## Table of Contents

1. [Tools Overview](#tools-overview)
2. [Resume Tools](#resume-tools)
3. [Job Search Tools](#job-search-tools)
4. [Career Planning Tools](#career-planning-tools)
5. [Interview Preparation](#interview-preparation)
6. [Market Intelligence](#market-intelligence)
7. [Combined Workflows](#combined-workflows)
8. [Prompt Templates](#prompt-templates)

---

## Tools Overview

| Tool | Purpose | Input | Output |
|------|---------|-------|--------|
| `parse_resume` | Extract structured data from resume text | Raw resume text | Name, skills, experience, education |
| `improve_resume` | Get AI suggestions to strengthen resume | Resume text + optional target role | Summary, bullet points, skill suggestions |
| `scrape_job_listing` | Extract job data from any URL | Job posting URL | Title, company, description, salary |
| `score_jobs_for_candidate` | Match resume to jobs | Resume + list of jobs | 0-100 scores with match reasons |
| `compare_jobs` | Side-by-side job comparison | 2+ job listings | Strengths, risks, recommendation |
| `skill_gap_analysis` | Find missing skills for target role | Resume + target role | Missing skills, resources, roadmap |
| `career_path` | Get career progression plan | Resume | Next role, skills, certs, timeline |
| `salary_estimate` | Estimate salary range | Skills, years, location | Min/max salary, confidence, factors |
| `generate_interview_questions` | Create interview prep questions | Job description + optional resume | Technical, behavioral, follow-up |
| `job_market_analysis` | Analyze hiring trends | Industry + optional location | Demand skills, salary ranges |
| `skill_demand_analysis` | Analyze skill market demand | List of skills | Demand level, growth, insights |

---

## Resume Tools

### 1. Parse Resume

Extract structured data from raw resume text.

```
Parse my resume:
[PASTE FULL RESUME TEXT HERE]
```

**Variations:**

```
# Basic parsing
Parse my resume: [paste resume]

# With email for follow-ups
Parse my resume:
[resume text]
Email me updates at: user@example.com

# Extract just skills
What skills does my resume highlight?
[resume text]
```

**Returns:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+1-555-0123",
  "location": "San Francisco, CA",
  "skills": ["Python", "JavaScript", "AWS", ...],
  "experience": [
    {
      "title": "Senior Engineer",
      "company": "Tech Corp",
      "start_date": "2020-01",
      "end_date": null,
      "description": "...",
      "bullet_points": [...]
    }
  ],
  "education": [...],
  "certifications": [...]
}
```

---

### 2. Improve Resume

Get AI suggestions to strengthen your resume.

```
Improve my resume for a [TARGET ROLE]:
[PASTE RESUME]
```

**Variations:**

```
# For a specific role
Improve my resume for a Senior ML Engineer position:
[resume]

# For a career transition
Improve my resume for a Product Manager role:
[resume]

# Without target (general improvement)
Improve my resume:
[resume]

# Focus on a specific section
Strengthen the professional summary and bullet points in my resume:
[resume]
```

**Returns:**
```json
{
  "summary": "Stronger professional summary with quantified impact...",
  "bullet_points": [
    "Led team of 5 engineers, delivering 3 major projects...",
    "Reduced latency by 40% through architectural improvements..."
  ],
  "suggested_skills": ["Kubernetes", "Terraform", "System Design"]
}
```

---

## Job Search Tools

### 3. Scrape Job Listing

Extract structured data from any job posting URL.

```
Scrape this job listing: [URL]
```

**Supported Sources:**
- LinkedIn
- Indeed
- Glassdoor
- WeWorkRemotely
- RemoteOK
- Generic webpages

**Variations:**

```
# Single job
Scrape: https://www.linkedin.com/jobs/view/123456789

# Multiple jobs
Scrape these jobs:
1. https://www.indeed.com/jobs?q=engineer&jlk=abc
2. https://www.glassdoor.com/job-listing/example
3. https://weworkremotely.com/remote-jobs/company-role
```

**Returns:**
```json
{
  "title": "Senior AI Engineer",
  "company": "TechAI Inc",
  "location": "San Francisco, CA (Remote)",
  "description": "We are looking for...",
  "url": "https://...",
  "salary_min": 150000,
  "salary_max": 200000,
  "currency": "USD",
  "posted_days_ago": 3,
  "source": "LinkedIn"
}
```

---

### 4. Score Jobs for Candidate

Compare multiple jobs against a resume for match scoring.

```
Score these jobs against my resume:
[PASTE RESUME]

Jobs:
1. [JOB URL or details]
2. [JOB URL or details]
3. [JOB URL or details]
```

**Full Workflow with Scraping:**

```
First, scrape these job listings:
- https://www.linkedin.com/jobs/view/123
- https://www.indeed.com/jobs/view/456

Then score them against my resume:
[PASTE RESUME]
```

**Variations:**

```
# Score by relevance
Which of these jobs is the best match for my background?
[resume]

- Senior ML Engineer at Anthropic: [url]
- AI Product Engineer at OpenAI: [url]
- Research Engineer at Google DeepMind: [url]

# Filter by threshold
Which of these jobs match me at 70%+?
[resume + job listings]
```

**Returns:**
```json
{
  "scored_jobs": [
    {
      "job": { "title": "...", "company": "...", ... },
      "score": 85.5,
      "match_reasons": [
        "5+ years ML experience aligns with requirements",
        "Python and PyTorch expertise directly applicable",
        "Led team of 4, exceeding the 3+ years management requirement"
      ],
      "weaknesses": [
        "Missing direct LLM fine-tuning experience",
        "No published research papers (preferred but not required)"
      ]
    }
  ],
  "summary": "The best matching role is..."
}
```

---

### 5. Compare Jobs

Side-by-side comparison of 2+ job listings.

```
Compare these two jobs:
[JOB 1 DETAILS OR URL]
[JOB 2 DETAILS OR URL]
```

**Full Workflow:**

```
Compare these three AI engineering roles:

Job 1: [paste job listing or URL]
Job 2: [paste job listing or URL]
Job 3: [paste job listing or URL]

I want to compare: salary, growth potential, work-life balance, and tech stack.
```

**Returns:**
```json
{
  "strengths": {
    "Job 1": ["Higher salary range", "Direct LLM work"],
    "Job 2": ["Better equity", "Series A startup"]
  },
  "risks": {
    "Job 1": ["High pressure environment", "On-site only"],
    "Job 2": ["Unproven product market fit"]
  },
  "salary_comparison": {
    "Job 1": {"min": 180000, "max": 220000},
    "Job 2": {"min": 150000, "max": 190000}
  },
  "skill_overlap": ["Python", "PyTorch", "MLOps", "AWS"],
  "overall_recommendation": "Job 1 is recommended if salary is priority..."
}
```

---

## Career Planning Tools

### 6. Skill Gap Analysis

Identify missing skills for a target role.

```
Analyze what skills I'm missing for a [TARGET ROLE]:
[PASTE RESUME]
```

**Variations:**

```
# Any tech role
What skills am I missing for a Staff Engineer role?
[resume]

# Leadership role
Skill gap analysis for an Engineering Manager position:
[resume]

# Career switch
What skills do I need for a Data Scientist -> ML Engineer transition?
[resume]

# Specific company/role
Gap analysis for Meta's Senior ML Engineer L5:
[resume]
```

**Returns:**
```json
{
  "current_skills": ["Python", "TensorFlow", "SQL", "AWS"],
  "missing_skills": [
    {
      "skill": "Distributed Training",
      "importance": "High",
      "resources": ["Coursera ML Engineering", "AWS SageMaker docs"]
    },
    {
      "skill": "Kubernetes",
      "importance": "Medium",
      "resources": ["KCNA certification", "K8s the Hard Way"]
    }
  ],
  "roadmap": [
    {
      "skill": "Distributed Training",
      "resources": ["Coursera: ML Engineering", "Blog: PyTorch DDP"],
      "timeline": "2-3 months",
      "priority": "High"
    }
  ]
}
```

---

### 7. Career Path

Generate career progression plan from resume.

```
What's my next career step based on my resume?
[PASTE RESUME]
```

**Variations:**

```
# Standard progression
Generate a career path from my resume:
[resume]

# With specific goal
I want to reach Director level in 3 years. What's my path?
[resume]

# Transition planning
Plan my transition from backend to AI/ML engineering:
[resume]
```

**Returns:**
```json
{
  "next_role": "Staff AI Engineer",
  "skills_needed": [
    "System Design for ML",
    "MLOps & Model Serving",
    "Team Leadership",
    "Distributed Training"
  ],
  "certifications": [
    "AWS ML Specialty",
    "Google Professional ML Engineer"
  ],
  "timeline_months": 12
}
```

---

### 8. Salary Estimate

Estimate salary based on skills, experience, and location.

```
Estimate my salary:
Skills: Python, LangChain, PyTorch, AWS, Kubernetes
Experience: 5 years
Location: San Francisco, CA
```

**Variations:**

```
# Remote position
Salary estimate for remote AI engineer:
Skills: Python, OpenAI API, FastAPI, PostgreSQL
Experience: 4 years
Location: USA (remote)

# With specific tech
What's the market rate for someone with:
- Python, JavaScript, React, Node.js
- 6 years experience
- Austin, TX

# Compare locations
Compare AI engineer salaries: NYC vs Seattle vs London
Skills: Python, TensorFlow, SQL
Experience: 3 years
```

**Returns:**
```json
{
  "min": 145000,
  "max": 185000,
  "currency": "USD",
  "confidence": "high",
  "factors": [
    "LangChain experience adds 15% premium",
    "AWS proficiency aligns with market demand",
    "5 years experience is optimal for Senior level"
  ]
}
```

---

## Interview Preparation

### 9. Generate Interview Questions

Create interview questions for a job description.

```
Generate interview questions for this job:
[PASTE JOB DESCRIPTION]
```

**Variations:**

```
# Standard questions
Generate interview questions for:
[JOB DESCRIPTION]

# Personalized to resume
Generate personalized interview questions using my background:
[JOB DESCRIPTION]

My resume:
[RESUME]

# Focus areas
Generate technical deep-dive questions for this ML Engineer role:
[JOB DESCRIPTION]

# Behavioral focus
Behavioral interview questions for a startup AI company:
[JOB DESCRIPTION]
```

**Returns:**
```json
{
  "technical": [
    "Explain the transformer architecture and its key components",
    "How would you debug a model that's overfitting?",
    "Design a RAG system for a knowledge base of 1M documents",
    "What is your experience with model fine-tuning?"
  ],
  "behavioral": [
    "Tell me about a time you had to explain ML concepts to non-technical stakeholders",
    "Describe a project where you had to balance accuracy vs. latency trade-offs"
  ],
  "follow_up": [
    "What ML frameworks do you prefer and why?",
    "How do you stay current with AI/ML research?"
  ]
}
```

**Advanced Usage - Mock Interview:**

```
Let's do a mock interview for this role.

First, generate questions:
[JOB DESCRIPTION]

Then I'll answer, and you provide feedback on my responses.
```

---

## Market Intelligence

### 10. Job Market Analysis

Analyze hiring trends for an industry and location.

```
Analyze the AI/ML job market in San Francisco.
```

**Variations:**

```
# General tech market
Job market analysis for software engineering in Austin, TX

# Remote focus
Remote software engineering market trends 2024

# Specific role type
Market analysis for full-stack developer roles in NYC

# Startup vs enterprise
Compare the hiring market: FAANG vs startup

# Include global
Global AI engineering market trends
```

**Returns:**
```json
{
  "trend": "Growing",
  "demand_skills": [
    "Python", "TypeScript", "React", "AWS", "Kubernetes"
  ],
  "salary_range": {
    "min": 120000,
    "max": 250000,
    "currency": "USD",
    "median": 175000
  },
  "insights": [
    "AI/ML skills command 20-30% premium over general software",
    "Remote positions increasing 15% YoY",
    "Kubernetes demand up 40% in past year"
  ]
}
```

---

### 11. Skill Demand Analysis

Analyze market demand for specific skills.

```
Analyze the demand for these skills:
- Python
- LangChain
- PyTorch
- Kubernetes
- AWS
```

**Variations:**

```
# Compare related skills
Demand analysis: React vs Vue vs Angular

# Emerging skills
What's the market demand for:
- LLM fine-tuning
- RAG systems
- Vector databases

# Data science skills
Skill demand comparison:
- SQL vs NoSQL
- TensorFlow vs PyTorch
- Tableau vs PowerBI
```

**Returns:**
```json
{
  "skill_demands": [
    {
      "skill": "Python",
      "demand": "High",
      "growth_trend": "Stable",
      "insights": "Most requested language for ML/data roles"
    },
    {
      "skill": "LangChain",
      "demand": "High",
      "growth_trend": "Rapidly Growing",
      "insights": "Newer skill but seeing rapid adoption for LLM apps"
    }
  ]
}
```

---

## Combined Workflows

### Complete Job Search Workflow

```
1. Parse my resume:
[PASTE RESUME]

2. Analyze skill gaps for Senior AI Engineer roles

3. Scrape these jobs:
- [LinkedIn URL 1]
- [Indeed URL 2]
- [WeWorkRemotely URL 3]

4. Score the scraped jobs against my resume

5. Compare the top 2 matches

6. Generate interview questions for the highest-scoring job
```

### Career Transition Workflow

```
I'm currently a [CURRENT ROLE] and want to transition to [TARGET ROLE].

1. Parse my resume:
[PASTE RESUME]

2. What skills do I need to develop?
[Target role description or just title]

3. Create a learning roadmap with timeline and resources

4. Estimate my future salary once I acquire these skills

5. Find jobs that bridge my current experience to the target role
```

### Offer Negotiation Workflow

```
I have two job offers. Compare them:
[OFFER 1 DETAILS]
[OFFER 2 DETAILS]

Include:
- Total compensation comparison
- Growth potential analysis
- Work-life balance factors
- Skill development opportunities

Then help me negotiate the better offer.
```

### Interview Prep Full Workflow

```
1. Scrape: [JOB URL]

2. Score against my resume:
[RESUME]

3. Generate technical and behavioral interview questions

4. For each technical question, provide:
   - What the interviewer wants to hear
   - Example answer structure
   - Common mistakes to avoid

5. Create a study plan for any skill gaps
```

---

## Prompt Templates

### Template 1: Initial Resume Analysis

```
Act as a career intelligence assistant. Analyze this resume and tell me:
1. What roles/level does this resume target?
2. What are the strongest skills?
3. What improvements would make this resume more competitive?
4. What salary range should this person expect?

Resume:
[PASTE RESUME]
```

### Template 2: Job Application Strategy

```
I want to apply to [COMPANY/TYPE OF COMPANIES].

Given my resume:
[PASTE RESUME]

1. Which roles should I target?
2. What should I emphasize in my application?
3. What gaps do I need to address?
4. What's the expected timeline to prepare?
```

### Template 3: Salary Negotiation Prep

```
I'm negotiating a job offer. Help me:

1. First, estimate fair market salary:
   Skills: [LIST]
   Experience: X years
   Location: [CITY/REMOTE]

2. Based on this offer:
   [OFFER DETAILS]

3. What points should I negotiate?
4. Provide specific talking points and counter-arguments.

5. What's a reasonable counter-offer range?
```

### Template 4: Weekly Job Search Review

```
Help me review my job search this week:

1. I applied to these roles:
   - [JOB 1] - status: [applied/interviewing/rejected]
   - [JOB 2] - status: [applied/interviewing/rejected]

2. I got these interview questions from:
   [LIST OR PASTE]

3. Help me prepare better answers for:
   - [QUESTION 1]
   - [QUESTION 2]

4. What should I focus on learning this week to improve my chances?
```

### Template 5: Career Annual Review Prep

```
It's time for my annual career review at [COMPANY].

My current role: [TITLE]
My resume: [PASTE]

1. What accomplishments should I highlight?
2. What new skills have I developed this year?
3. What's a fair self-assessment rating?
4. What should I ask for in terms of promotion/raise?
5. If I don't get what I want, what's my exit plan?
```

### Template 6: Technical Interview Coach

```
I'm preparing for a technical interview at [COMPANY] for [ROLE].

Job description: [PASTE OR LINK]

My background: [RELEVANT EXPERIENCE BRIEF]

I want to:
1. Generate realistic interview questions
2. Practice answering them
3. Get feedback on my answers
4. Know what to study more

Let's start with [SPECIFIC TOPIC, e.g., "system design for ML"].
```

### Template 7: Remote Job Search

```
I'm specifically looking for remote opportunities.

1. Parse my resume:
[PASTE RESUME]

2. Which remote-friendly roles should I target?

3. Find remote jobs on these platforms:
   - WeWorkRemotely
   - RemoteOK
   - Turing
   - FlexJobs

   Search for: [KEYWORDS]

4. What's different about remote resume optimization?

5. How should I prepare for remote-specific interview questions?
```

### Template 8: Interview Follow-Up

```
I just finished an interview for [ROLE] at [COMPANY].

The interviewer asked:
[QUESTION 1]: [YOUR ANSWER]
[QUESTION 2]: [YOUR ANSWER]
[QUESTION 3]: [YOUR ANSWER]

How did I do? What were the strengths and weaknesses of my answers?
What should I have said differently?
```

### Template 9: Burnout & Career Pivot

```
I'm feeling burnt out in my current role and considering a pivot.

Current situation:
- Role: [TITLE]
- Years in field: X
- Burnout signs: [SYMPTOMS]

I'm considering:
1. [OPTION A: e.g., Pivot to management]
2. [OPTION B: e.g., Switch to a less demanding company]
3. [OPTION C: e.g., Career change to new industry]

What factors should I consider? Help me weigh the options.
```

### Template 10: Startup vs Big Tech Decision

```
I have offers from:

Startup: [COMPANY/DETAILS]
- Equity: X%
- Salary: $Y
- Stage: [SEED/A/B/etc]
- Risk: [HIGH/MEDIUM/LOW]

Big Tech: [COMPANY/DETAILS]
- Equity: X options
- Salary: $Y
- Level: [L4/L5/etc]
- Stability: [HIGH/MEDIUM/LOW]

Help me compare:
1. Total compensation over 4 years
2. Career growth potential
3. Work-life balance
4. Learning opportunities
5. Risk tolerance advice

I'm [X] years old and my priorities are [LIST].
```

---

## Quick Reference Commands

### Emergency Interview Prep (30 minutes)

```
1. "Score my resume against this job: [URL]"
2. "Generate 5 technical and 5 behavioral questions"
3. "Give me quick feedback on my answers to: [question]"
```

### Weekend Career Check-In

```
1. "Parse my resume and tell me my top 3 strengths"
2. "What's the market rate for my skills in [location]?"
3. "Find 3 remote jobs I should apply to this week"
4. "What should I learn next to increase my value?"
```

### Monthly Market Intelligence

```
1. "Analyze the job market for [YOUR FIELD]"
2. "What's trending in [SKILL] right now?"
3. "Compare salaries: [CITY A] vs [CITY B] vs [CITY C]"
```

---

## Tips for Effective Use

1. **Paste full job descriptions** for better analysis - truncated descriptions lead to incomplete analysis.

2. **Include salary ranges** when scraping jobs - helps with more accurate comparisons.

3. **Use specific titles** in skill gap analysis - "Staff Engineer" vs "Senior Engineer" have different requirements.

4. **Combine tools** for comprehensive results - scraping + scoring + comparing gives the full picture.

5. **Save parsed data** - once your resume is parsed, reuse the structured data in follow-up questions.

6. **Iterate on resume improvements** - use the suggestions, then re-analyze for further improvements.

7. **Track market trends** - run skill demand analysis quarterly to stay current.

---

## Error Handling

If a tool fails:
- **scrape_job_listing**: Try with full URL, ensure it's publicly accessible
- **skill_demand_analysis**: Try individual skills instead of a long list
- **salary_estimate**: Be specific with location (city, state, remote)

---

*Last updated: June 21 2026*
