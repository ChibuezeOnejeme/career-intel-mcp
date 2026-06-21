# Career Intelligence MCP

An AI-powered career intelligence platform for job seekers. Parse resumes, scrape and score job listings, analyze skill gaps, and prepare for interviews.

## Features

- **Resume Parsing** — Paste your resume text, get structured data (name, skills, experience, education)
- **Resume Improvement** — Get AI suggestions to strengthen your resume for a target role
- **Job Scraping** — Paste any job listing URL (LinkedIn, Indeed, Glassdoor, etc.) and get structured data
- **Job Scoring** — Compare multiple jobs against your resume and see match scores
- **Job Comparison** — Side-by-side comparison of 2-3 jobs (salary, skills, risks, recommendation)
- **Skill Gap Analysis** — Identify missing skills for a target role with a learning roadmap
- **Career Path** — Get a career progression plan based on your resume
- **Salary Estimation** — Estimate salary ranges based on skills, experience, and location
- **Interview Questions** — Generate technical, behavioral, and follow-up questions for any role
- **Market Analysis** — Analyze hiring trends and skill demand

## Requirements

- Python 3.12+
- An OpenRouter API key (free tier works)

## Setup

### 1. Clone and install dependencies

```bash
git clone <your-repo-url>
cd mcp-intel
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -e .
```

### 2. Configure environment

```bash
cp .env.example .env
# Edit .env with your settings:
# LLM_API_KEY=your_openrouter_api_key
# DATABASE_URL is already set to use SQLite (career_intel.db)
```

### 3. Get an OpenRouter API key

1. Sign up at [openrouter.ai](https://openrouter.ai)
2. Go to Keys → Create key
3. Add to `.env` as `LLM_API_KEY=sk-or-...`

Default model is `deepseek/deepseek-chat` (free tier, works well). You can change `LLM_MODEL` in `.env` to any OpenRouter model.

### 4. Run the app

```bash
python -m app.main
# Database (career_intel.db) auto-creates on first run
```

That's it — no database setup needed. The SQLite file (`career_intel.db`) is created automatically.

---

## Deployment Options

Choose the option that fits your setup.

### Option 1: Local HTTP Server (Development)

The server runs as an HTTP server on `localhost:8000`. Connect to it using any HTTP-capable MCP client.

```bash
python -m app.main
# Server starts on http://0.0.0.0:8000
```

---

### Option 2: Stdio Mode (Direct MCP Connection)

Run as a stdio MCP server. This connects directly to an MCP client like Claude Desktop without needing HTTP.

```bash
python -m app.main --transport stdio
```

**For Claude Desktop**, add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "career-intel": {
      "command": "/full/path/to/venv/bin/python",
      "args": ["-m", "app.main", "--transport", "stdio"]
    }
  }
}
```

**Setup steps:**
1. Run the server in stdio mode or use Claude Desktop config above
2. Restart Claude Desktop

---

### Option 3: Cloudflare Tunnel (Remote Access)

Expose your locally-running server to the internet securely using Cloudflare Tunnel — no public IP, account, or firewall needed.

**Step 1: Install cloudflared**

```bash
# macOS
brew install cloudflare/cloudflare/cloudflared

# Linux
curl -L https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -o cloudflared
chmod +x cloudflared
sudo mv cloudflared /usr/local/bin/
```

**Step 2: Start the app**
```bash
python -m app.main
```

**Step 3: Start the tunnel**
```bash
cloudflared access --url http://localhost:8000
# You'll see output like:
# Your tunnel Qo7xG@example.app.link
```

**Step 4: Connect Claude Desktop**

```json
{
  "mcpServers": {
    "career-intel": {
      "command": "cloudflared",
      "args": ["access", "--url", "http://localhost:8000"]
    }
  }
}
```

**Setup steps:**
1. Install cloudflared
2. Start the app (`python -m app.main`)
3. Start cloudflared tunnel
4. Add to Claude Desktop config
5. Restart Claude Desktop

---

### Option 4: ngrok Tunnel (Remote Access)

Expose your locally-running server via ngrok. Requires an ngrok account (free tier works).

**Step 1: Install ngrok**

```bash
# macOS
brew install ngrok

# Linux
curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null
echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list
sudo apt update && sudo apt install ngrok
```

**Step 2: Sign up and get your authtoken**

1. Sign up at [ngrok.com](https://ngrok.com)
2. Copy your authtoken from the dashboard
3. Configure it: `ngrok config add-authtoken YOUR_TOKEN`

**Step 3: Start the app**
```bash
python -m app.main
```

**Step 4: Start ngrok**
```bash
ngrok http 8000
# You'll see output like:
# Forwarding  https://abc123.ngrok.io -> http://localhost:8000
```

**Step 5: Connect Claude Desktop**

```json
{
  "mcpServers": {
    "career-intel": {
      "command": "ngrok",
      "args": ["http", "--domain", "your-ngrok-subdomain.ngrok.io", "8000"]
    }
  }
}
```

**Setup steps:**
1. Install ngrok and create an account
2. Add your authtoken: `ngrok config add-authtoken YOUR_TOKEN`
3. Start the app (`python -m app.main`)
4. Start ngrok (`ngrok http 8000`)
5. Add to Claude Desktop config
6. Restart Claude Desktop

---

## Connecting to Claude Desktop

After setting up your preferred deployment option, add to Claude Desktop:

```json
{
  "mcpServers": {
    "career-intel": {
      "command": "/full/path/to/venv/bin/python",
      "args": ["-m", "app.main", "--transport", "stdio"]
    }
  }
}
```

**Or** if using a tunnel (cloudflared or ngrok):

```json
{
  "mcpServers": {
    "career-intel": {
      "command": "cloudflared",
      "args": ["access", "--url", "http://localhost:8000"]
    }
  }
}
```

Then **restart Claude Desktop**.

---

## Usage Examples

### Parse your resume

```
User: Parse my resume:
[Full resume text pasted here]

Assistant calls: parse_resume(raw_text="...")
Returns: { name, email, skills, experience, education, ... }
```

### Scrape a job listing

```
User: Scrape this job: https://www.linkedin.com/jobs/view/12345

Assistant calls: scrape_job_listing(url="...")
Returns: { title, company, location, description, salary_min, salary_max, ... }
```

### Score jobs against your resume

```
User: Score these jobs for me [paste resume] [paste job URLs]

Assistant calls:
1. scrape_job_listing(url="...") — for each URL
2. score_jobs_for_candidate(resume_text="...", jobs=[...])
Returns: [{ job, score (0-100), match_reasons, weaknesses }, ...]
```

### Compare jobs

```
User: Compare these 2 jobs [paste job details]

Assistant calls: compare_jobs(jobs=[...])
Returns: { strengths, risks, salary_comparison, skill_overlap, overall_recommendation }
```

### Prepare for interviews

```
User: Generate interview questions for this job [paste job description]

Assistant calls: generate_interview_questions(job_description="...")
Returns: { technical: [...], behavioral: [...], follow_up: [...] }
```

### Analyze skill gaps

```
User: What skills am I missing for a Staff Engineer role? [paste resume]

Assistant calls: skill_gap_analysis(resume_text="...", target_role="Staff Engineer")
Returns: { current_skills, missing_skills, roadmap: [{ skill, resources, timeline, priority }] }
```

---

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `DATABASE_URL` | `sqlite+aiosqlite:///./career_intel.db` | SQLite database path |
| `LLM_API_KEY` | (empty) | OpenRouter API key |
| `LLM_MODEL` | `deepseek/deepseek-chat` | OpenRouter model to use |
| `LLM_BASE_URL` | `https://openrouter.ai/api/v1` | OpenRouter base URL |
| `LOG_LEVEL` | `INFO` | Logging level |

---

## API Endpoints

- `GET /health` — Health check. Returns database and LLM status.

---

## Architecture

- **FastMCP** — Server framework
- **SQLAlchemy (async)** — Database ORM
- **SQLite** — Local database (no server setup)
- **OpenRouter** — LLM calls (DeepSeek, Claude, etc.)
- **httpx + BeautifulSoup** — Job listing scraping
