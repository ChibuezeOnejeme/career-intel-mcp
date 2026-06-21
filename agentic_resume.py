from fpdf import FPDF

class ResumePDF(FPDF):
    def header(self):
        pass
    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')

pdf = ResumePDF()
pdf.add_page()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.set_left_margin(15)
pdf.set_right_margin(15)

# NAME & TITLE
pdf.set_font('Helvetica', 'B', 18)
pdf.cell(0, 10, 'AGENTIC AI ENGINEER', new_x='LMARGIN', new_y='NEXT', align='C')
pdf.set_font('Helvetica', '', 10)
pdf.cell(0, 5, 'AI Solutions Engineer | LLM Agents | Agentic Workflows | Production AI Systems', new_x='LMARGIN', new_y='NEXT', align='C')
pdf.set_font('Helvetica', '', 8)
pdf.cell(0, 4, 'Lagos, Nigeria  |  onejemechibueze33@gmail.com  |  github.com/ChibuezeOnejeme  |  linkedin.com/in/chibuezeonejeme', new_x='LMARGIN', new_y='NEXT', align='C')
pdf.ln(3)

# SUMMARY
pdf.set_font('Helvetica', 'B', 10)
pdf.cell(0, 6, 'PROFESSIONAL SUMMARY', new_x='LMARGIN', new_y='NEXT')
pdf.set_font('Helvetica', '', 8)
pdf.multi_cell(0, 4, 'Agentic AI Engineer with 4+ years building production LLM-powered applications, autonomous agents, and agentic workflows. Specialized in designing multi-agent systems, RAG pipelines, and conversational AI platforms using LangChain, CrewAI, and LlamaIndex. Deep expertise in deploying scalable AI solutions with vector databases (Pinecone, Weaviate) and cloud-native technologies. 7 years of leadership experience translates business requirements into scalable AI solutions.')
pdf.ln(2)

# TECHNICAL SKILLS
pdf.set_font('Helvetica', 'B', 10)
pdf.cell(0, 6, 'TECHNICAL SKILLS', new_x='LMARGIN', new_y='NEXT')
pdf.set_font('Helvetica', '', 8)

skills = [
    ('Agentic AI & Frameworks', 'LangChain, CrewAI, LlamaIndex, AutoGPT, Hugging Face, AutoGen, Semantic Kernel'),
    ('LLM & AI APIs', 'OpenAI API, Anthropic Claude, Ollama, Together AI, Vercel AI SDK, Google Gemini'),
    ('Agent Architecture', 'Multi-agent systems, Tool use, ReAct agents, Planning agents, Memory systems, RAG'),
    ('Programming & Backend', 'Python, JavaScript, FastAPI, Django, REST APIs, GraphQL, PostgreSQL, Redis'),
    ('Vector & Data', 'Pinecone, Weaviate, Supabase Vector, ChromaDB, Qdrant, Pandas, SQL'),
    ('DevOps & Deployment', 'Docker, Kubernetes, GitHub Actions, AWS, GCP, Vercel, Railway'),
]

y_start = pdf.get_y()
label_width = 45

for label, val in skills:
    pdf.set_font('Helvetica', 'B', 8)
    pdf.cell(label_width, 4, label + ':', new_x='RIGHT', new_y='TOP')
    pdf.set_font('Helvetica', '', 8)
    x_after_label = pdf.get_x()
    remaining_width = pdf.w - x_after_label - pdf.r_margin
    pdf.multi_cell(remaining_width, 4, val)
    pdf.set_y(pdf.get_y() + 1)

pdf.ln(2)

# EXPERIENCE
pdf.set_font('Helvetica', 'B', 10)
pdf.cell(0, 6, 'PROFESSIONAL EXPERIENCE', new_x='LMARGIN', new_y='NEXT')

# Core360
pdf.set_font('Helvetica', 'B', 9)
pdf.cell(0, 5, 'AI Specialist & Solutions Engineer  |  Core360  |  01/2021 - Present  |  Remote', new_x='LMARGIN', new_y='NEXT')
bullets = [
    'Architected and deployed 8+ production AI agent systems using LangChain and CrewAI, automating complex business workflows for 500+ enterprise clients',
    'Built multi-agent orchestration platforms with tool-use, planning, and long-term memory for autonomous task completion',
    'Developed RAG pipelines with Pinecone and Weaviate, reducing query response time by 70% while improving accuracy',
    'Created conversational AI platforms using OpenAI and Anthropic APIs, handling 10K+ daily conversations with 95% satisfaction',
    'Deployed scalable AI microservices on Kubernetes with GitHub Actions CI/CD, achieving 99.9% uptime',
    'Led technical discovery and PoC development, converting 70% of prospects through AI demonstrations',
]
for b in bullets:
    pdf.set_x(18)
    pdf.multi_cell(0, 3.8, '- ' + b)
pdf.ln(1)

# Datamagic Project
pdf.set_font('Helvetica', 'B', 9)
pdf.cell(0, 5, 'AI Business Intelligence Platform (PoC)  |  Datamagic.xyz', new_x='LMARGIN', new_y='NEXT')
pdf.set_x(18)
pdf.set_font('Helvetica', '', 8)
pdf.multi_cell(0, 3.8, '- Designed LLM-powered SQL copilot and analytics agents for natural language to database queries; integrated real-time visualization dashboards')

pdf.ln(1)

# Learnorita Project
pdf.set_font('Helvetica', 'B', 9)
pdf.cell(0, 5, 'AI-Powered Learning Platform (PoC)  |  Learnorita.com', new_x='LMARGIN', new_y='NEXT')
pdf.set_x(18)
pdf.set_font('Helvetica', '', 8)
pdf.multi_cell(0, 3.8, '- Built autonomous learning assistant using agentic workflows with personalized content recommendation and intelligent tutoring agents')

pdf.ln(1)

# Sales Leadership
pdf.set_font('Helvetica', 'B', 9)
pdf.cell(0, 5, 'Sales Team Lead  |  Anheuser-Busch  |  10/2013 - 12/2020', new_x='LMARGIN', new_y='NEXT')
pdf.set_x(18)
pdf.set_font('Helvetica', '', 8)
pdf.multi_cell(0, 3.8, '- Led team of 11 BDRs overseeing 2,200+ outlets; managed $4M+ credit facility; achieved double-digit revenue growth')
pdf.ln(2)

# EDUCATION & CERTIFICATIONS
pdf.set_font('Helvetica', 'B', 10)
pdf.cell(90, 6, 'EDUCATION', new_x='RIGHT', new_y='TOP')
pdf.set_font('Helvetica', 'B', 10)
pdf.cell(0, 6, 'CERTIFICATIONS', new_x='LMARGIN', new_y='NEXT')
pdf.set_font('Helvetica', '', 8)
pdf.cell(90, 4, 'B.S. Marketing, Nnamdi Azikiwe University', new_x='RIGHT', new_y='TOP')
pdf.cell(0, 4, 'AWS Cloud Practitioner (in progress)', new_x='LMARGIN', new_y='NEXT')
pdf.cell(90, 4, '', new_x='RIGHT', new_y='TOP')
pdf.cell(0, 4, 'Google Cloud Professional ML Engineer (planned)', new_x='LMARGIN', new_y='NEXT')

output_path = '/home/eze/repos/mcp-intel/Agentic_AI_Engineer_Resume.pdf'
pdf.output(output_path)
print(f'PDF created: {output_path}')