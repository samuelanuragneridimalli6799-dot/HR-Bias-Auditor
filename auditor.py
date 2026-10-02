import os
import json
import re
import time
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import List
from google import genai
from google.genai import types

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY is missing! Please set it in your .env file.")

client = genai.Client(api_key=api_key)

# 1. Structured Output Schemas
class BiasFlag(BaseModel):
    category: str = Field(description="e.g., 'Gender Coded', 'Ageist Proxy', 'Socioeconomic Proxy', 'Ableist'")
    flagged_phrase: str = Field(description="Exact phrase or requirement from the text")
    explanation: str = Field(description="Why this creates adverse impact or regulatory non-compliance")
    suggested_replacement: str = Field(description="Neutral, competency-based replacement")

class AuditResult(BaseModel):
    overall_fairness_score: int = Field(description="Fairness score from 0 (heavily biased) to 100 (fully neutral)")
    risk_level: str = Field(description="'Low', 'Medium', or 'High' risk under EU AI Act employment standards")
    summary: str = Field(description="Executive summary of the audit findings")
    flags: List[BiasFlag] = Field(description="List of detected exclusionary or biased items")
    inclusive_rewrite: str = Field(description="Fully revised version of the job description")

# 2. Deterministic Lexicon Check
AGENTIC_WORDS = [
    "rockstar", "ninja", "guru", "dominant", "aggressive", "assertive",
    "driven", "outspoken", "competitive", "superior", "relentless", "fast-paced"
]

COMMUNAL_WORDS = [
    "collaborative", "supportive", "nurturing", "sensitive", "interpersonal",
    "compassionate", "caring", "warm", "empathetic"
]

def check_lexicon(text: str) -> dict:
    text_lower = text.lower()
    found_agentic = [w for w in AGENTIC_WORDS if re.search(rf"\b{w}\b", text_lower)]
    found_communal = [w for w in COMMUNAL_WORDS if re.search(rf"\b{w}\b", text_lower)]
    return {
        "agentic_flags": list(set(found_agentic)),
        "communal_flags": list(set(found_communal))
    }

SYSTEM_INSTRUCTION = """
You are a Senior HR Compliance Officer and Algorithmic Bias Specialist.
Your task is to audit job postings and candidate screening rubrics for:
1. Demographic & Age Bias (e.g., 'digital native', 'recent graduate', 'high stamina').
2. Gender bias (overly masculine/agentic phrasing).
3. Socioeconomic & Educational proxies (e.g., requiring elite universities over demonstrable competency).
4. Accessibility / Ableist language (e.g., 'must lift 50 lbs' when non-essential).
5. Regulatory risk under the EU AI Act (High-Risk AI system classification for HR & recruitment) and EEOC guidelines.
"""

# Models to try in order if one experiences a temporary spike
CANDIDATE_MODELS = [
    "gemini-3.5-flash-lite",
    "gemini-3.8-flash",
    "gemini-3.1-pro"
]

def audit_job_posting(job_title: str, text: str) -> dict:
    lexicon_stats = check_lexicon(text)

    prompt = f"""
    Target Job Title: {job_title}

    Text to Audit:
    \"\"\"
    {text}
    \"\"\"

    Deterministic Lexicon Findings:
    - Masculine/agentic keywords: {lexicon_stats['agentic_flags']}
    - Communal keywords: {lexicon_stats['communal_flags']}

    Perform a full compliance audit and provide an inclusive rewrite.
    """

    last_error = None
    for model_name in CANDIDATE_MODELS:
        try:
            print(f"Connecting to model: {model_name}...")
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_INSTRUCTION,
                    response_mime_type="application/json",
                    response_schema=AuditResult,
                    temperature=0.1,
                )
            )
            result_dict = json.loads(response.text)
            result_dict["lexicon_stats"] = lexicon_stats
            print(f"Audit completed successfully via {model_name}!")
            return result_dict
        except Exception as e:
            print(f"Model {model_name} failed or busy ({e}). Trying fallback...")
            last_error = e
            time.sleep(1)

    raise last_error