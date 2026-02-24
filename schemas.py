from pydantic import BaseModel, Field
from typing import List, Dict

class ATSResult(BaseModel):
    overall_score: int = Field(ge=0, le=100)
    category_scores: Dict[str, int]
    missing_required_skills: List[str]
    weak_areas: List[str]
    strong_matches: List[str]
    risk_flags: List[str]
    summary: str

class ResumeFacts(BaseModel):
    skills: List[str]
    tools: List[str]
    protocols: List[str]
    domains: List[str]
    responsibilities: List[str]

class RewrittenResumeSections(BaseModel):
    summary: str
    hard_skills: List[str]
    projects: Dict[str, List[str]]