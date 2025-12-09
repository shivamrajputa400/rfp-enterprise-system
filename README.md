# AI RFP Web Scraper & Processing System
## EY Techathon 2025 – Enterprise Agentic AI Workflow

---

# 1. Introduction
A modular, enterprise-grade system for:
- Web scraping
- Content extraction
- PDF generation
- Direct integration into an RFP automation pipeline

Designed to match the EY-style professional design language.

---

# 2. Features

## 2.1 Web Scraper Capabilities
- URL input & validation
- Configurable scraping depth
- Content type selection (Text / HTML / JSON)
- Real-time scraping progress
- In-browser content preview
- Word count, heading map, link map statistics
- EY-style PDF generation
- Recent scrape history
- Mock APIs for Techathon demo mode

## 2.2 RFP Integration Layer
- Scraped content → PDF → RFP pipeline
- Automatic ingestion into multi-agent system
- Clean error boundaries
- Consistent design with main RFP solution

---

# 3. Architecture Overview

## 3.1 High-Level Flow
Web UI  
→ Scraper Engine  
→ Content Cleaner  
→ PDF Generator  
→ RFP Pipeline  
→ Multi-Agent System  
→ Final Response

## 3.2 Component-Based Architecture
- Scraper Engine (Puppeteer / Cheerio)
- Cleaner & Normalizer
- PDF Generator (HTML-to-PDF)
- RFP Integration Layer
- Agents (Technical / Pricing / Summarization)
- Storage Layer (Mongo/Postgres)
- Frontend React UI

---

# 4. Folder Structure
ai-rfp-web-scraper           
├── .env.example  
├── package.json  
└── README.md

---

# 5. Installation

## 5.1 Clone Repo
git clone https://github.com/shivamrajputa400/rfp-enterprise-system.git  
cd ai-rfp-web-scraper

## 5.2 Install Dependencies
npm install

## 5.3 Setup Environment
cp .env.example .env

---

# 6. Running the System

## 6.1 Start Backend
npm run server

## 6.2 Start Frontend
npm run dev

---

# 7. Workflow: Web Scraper → PDF → RFP AI Pipeline

## Step 1 — URL Submission
User submits URL → URL validated

## Step 2 — Scraping
Scraper fetches content  
Optional: depth=1 internal link crawling  

## Step 3 — Cleaning
HTML → normalized text  
Extract:
- headings  
- paragraphs  
- links  
- tables  

## Step 4 — Preview & Stats
User sees:
- Scraped text  
- Word count  
- Heading map  
- Link map  

## Step 5 — PDF Generation
Structured EY-format PDF created with:
- Title  
- URL  
- Content sections  
- Auto TOC  

## Step 6 — RFP Pipeline Integration
PDF delivered into RFP ingestion service  
Multi-agent chain processes document

---

# 8. Approach & Methodology (Aligned with EY Techathon)

## Step 1: RFP Discovery & Qualification
- Monitor PSU portals / URLs / emails  
- Extract metadata: project, deadlines, scope  
- Auto-qualify based on timelines & product relevance  

## Step 2: Contextual RFP Summarization
- Role-based summaries:
  - Technical agent: specs, scope  
  - Pricing agent: tests, costing  
  - Sales agent: submission requirements  
- Identify dependencies and critical paths  

## Step 3: Product–Spec Matching (Technical Agent)
- NLP parsing of specifications  
- Match against OEM datasheets  
- Compare attribute-by-attribute  
- Compute Spec Match Score (%)  
- Recommend best-fit SKUs  

## Step 4: Pricing & Cost Estimation (Pricing Agent)
- Generate price tables  
- Map required tests/services  
- Compute:
  - material cost  
  - testing/service cost  
- Return line-item costing  

## Step 5: Final RFP Response Assembly
- Merge technical + pricing output  
- SKU justification  
- Final structured RFP response  

---

# 9. Value Proposition
- 70–80% faster RFP turnaround  
- 2–3× more RFPs handled annually  
- Higher on-time submissions  
- Consistent SKU matching  
- Automated cost estimation  
- Scalable to multiple product categories  

---

# 10. Technology Stack

## Core Technology
- Node.js  
- Express  
- React / Next.js  
- PYTHON 
- Cheerio  
- HTML-to-PDF engine  

## AI Components
- LLM agents  
- Vector DB  
- RFP knowledge graph  

## Storage
- MongoDB  
- PostgreSQL  

---

# 11. Security & Compliance
- Role-based access control  
- Encrypted document storage  
- Sanitized HTML  
- Tamper-proof audit logs  

---

# 12. Roadmap
- Browser extension for instant scraping  
- Batch URL scraping  
- OCR for image-based RFPs  
- Auto email ingestion  
- Multi-language RFP support  
- RFP similarity clustering  
---

# 13. Maintainers
- TEAM AgenTriX  
- EY Techathon Team  


