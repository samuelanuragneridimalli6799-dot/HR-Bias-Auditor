# HR-Bias-Auditor
Algorithmic Fairness &amp; Bias Auditor for Job Descriptions and Recruitment Prompts
# 🛡️ HR Algorithmic Bias & Compliance Auditor

> An automated auditing engine evaluating job postings and candidate screening rubrics for adverse impact, demographic proxy variables, and regulatory alignment with **EU AI Act High-Risk Employment requirements** and **EEOC non-discrimination standards**.

---

## 📌 Problem Statement

Under the **EU AI Act**, algorithmic systems deployed in talent acquisition, screening, and worker evaluation are classified as **High-Risk (Annex III)**. Requisitions containing unvetted proxy variables, exclusionary tenure boundaries, or gender-coded phrasing introduce material regulatory and disparate-impact risks.

This project delivers a **hybrid deterministic and LLM-assisted audit pipeline** to programmatically detect exclusionary phrasing, quantify risk, and generate competency-based alternatives.

---

## ⚙️ System Architecture

[Job Description / Screening Rubric ]
│
▼
┌────────────────────────────────────────────────────────┐
│  Layer 1: Deterministic Lexicon Analysis               │
│  - Academic keyword scans (Agentic vs. Communal)      │
│  - Heuristic checks for exclusionary tenure markers     │
└──────────────────────────┬─────────────────────────────┘
│
▼
┌────────────────────────────────────────────────────────┐
│  Layer 2: LLM Regulatory Evaluation (Gemini Engine)    │
│  - Strict JSON schema enforcement via Pydantic        │
│  - Detection of age, gender, socioeconomic & ableist   │
│    proxies (e.g., 'digital native', elite pedigrees)   │
│  - Scoring against EU AI Act & EEOC rubrics           │
└──────────────────────────┬─────────────────────────────┘
│
▼
┌────────────────────────────────────────────────────────┐
│  Layer 3: Synthesizer & Streamlit Dashboard            │
│  - Composite Fairness Score (0–100)                    │
│  - Flagged risk cards with corrective recommendations  │
│  - Neutral, skills-based rewrite generator            │
└────────────────────────────────────────────────────────┘

## 🚀 Key Features

* **Dual-Layer Evaluation:** Combines deterministic regex matching (grounded in Gaucher et al. research on gendered wording) with structured LLM reasoning.
* **Guaranteed Schema Integrity:** Enforces Pydantic models for deterministic, reliable JSON responses.
* **Granular Proxy Detection:** Identifies ageist proxies (*digital native*), socioeconomic filters (*elite university pedigree*), ableist standards, and linguistic barriers.
* **Actionable Remediation:** Outputs a composite fairness score (0–100), risk tiering, and an automated inclusive rewrite.

---

## 🛠 Tech Stack

* **Language:** Python 3.11+
* **LLM Engine:** Google Gemini API (`google-genai`) with native structured outputs
* **Data Validation:** Pydantic v2
* **Frontend:** Streamlit
* **Environment & CI/CD:** GitHub Codespaces / Git

---

## 📦 Local Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/](https://github.com/)<YOUR-USERNAME>/HR-Bias-Auditor.git
   cd HR-Bias-Auditor