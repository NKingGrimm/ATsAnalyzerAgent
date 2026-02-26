import json
import ollama
from schemas import ATSResult, ResumeFacts, RewrittenResumeSections
from prompts import *

MAX_SCORES = {
    "core_requirements": 35,
    "role_relevance": 15,
    "tools_technologies": 15,
    "experience_level": 15,
    "keywords_phrasing": 10,
    "clarity_structure": 10,
}
ASSETS_PATH = "assets/"
RESUME_PATH = ASSETS_PATH + "resume.txt"
JOB_POSITION_PATH = ASSETS_PATH + "job_position.txt"

def _fact_extraction_from_resume(resume: str) -> ResumeFacts:
    prompt = FACT_EXTRACTION_PROMPT.format(
        resume_description=resume
    )

    response = ollama.chat(
        model="llama3.1:8b",
        messages=[
            {"role": "system", "content": FACT_EXTRACTION_SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        format="json"  # CRITICAL
    )

    try:
        raw = json.loads(response["message"]["content"])
        ats_result = ResumeFacts(**raw)
    except Exception as e:
        raise RuntimeError("Invalid JSON returned by Llama") from e
    return ats_result

def _enforce_balanced_rules(result: ATSResult) -> ATSResult:
    # Clamp category scores
    for cat, max_val in MAX_SCORES.items():
        result.category_scores[cat] = max(
            0, min(result.category_scores.get(cat, 0), max_val)
        )

    # Deterministic total
    result.overall_score = sum(result.category_scores.values())

    # Balanced penalties
    missing = len(result.missing_required_skills)
    if missing == 1:
        result.overall_score -= 5
    elif missing == 2:
        result.overall_score -= 10
    elif missing > 2:
        result.overall_score = min(result.overall_score, 69)

    result.overall_score = max(0, min(result.overall_score, 100))
    return result

def _score_resume_against_job(job_description: str, resume_description: str) -> ATSResult:
    prompt = USER_PROMPT_TEMPLATE.format(
        job_description = job_description,
        resume_description = resume_description
    )

    response = ollama.chat(
        model="llama3.1:8b",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        format="json"  # CRITICAL
    )

    try:
        raw = json.loads(response["message"]["content"])
        #FIXME: It is possible that the agen returns a float value for the overal_score
        ats_result = ATSResult(**raw)
    except Exception as e:
        raise RuntimeError("Invalid JSON returned by Llama") from e

    return _enforce_balanced_rules(ats_result)

def _decide_action(score: int) -> str:
    if score >= 70:
        return "APPLY_AS_IS"
    elif score >= 60:
        return "REWRITE_RESUME"
    else:
        return "SKIP"

def _rewrite_resume(
    resume_text: str,
    job_description: str,
    allowed_facts: dict,
    weak_areas: list,
    missing_skills: list
) -> str:

    # extractedFacts = fact_extraction_from_resume(resume_description)
    #     if action == "REWRITE_RESUME":
    #         rewriteContent = rewrite_resume(resume_description,
    #                                         job_description,
    #                                         extractedFacts.model_dump(),
    #                                         result.weak_areas,
    #                                         result.missing_required_skills)
    #         print(rewriteContent, end='\n')

    prompt = REWRITE_PROMPT_TEMPLATE.format(
        resume_text=resume_text,
        job_description=job_description,
        allowed_facts=json.dumps(allowed_facts, indent=2),
        weak_areas=weak_areas,
        missing_skills=missing_skills
    )

    response = ollama.chat(
        model="llama3.1:8b",
        messages=[
            {"role": "system", "content": REWRITE_SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ]
    )

    try:
        raw = json.loads(response["message"]["content"])
        rewrite_result = RewrittenResumeSections(**raw)
    except Exception as e:
        raise RuntimeError("Invalid JSON returned by Llama") from e
    # # Refusal handling
    # if '"refusal": true' in content:
    #     raise RuntimeError("Resume rewrite refused due to insufficient factual support")

    return rewrite_result

def analyze_resume_and_get_score():
    with open(JOB_POSITION_PATH, "r", encoding="utf-8") as f:
        job_description = f.read()

    with open(RESUME_PATH, "r", encoding="utf-8") as f:
        resume_description = f.read()

    result = _score_resume_against_job(job_description, resume_description)
    action = _decide_action(result.overall_score)
    return result, action

# def validate_no_new_skills(original_facts, rewritten_text):
#     for skill in rewritten_text.split():
#         if skill in SUSPICIOUS_SKILLS and skill not in original_facts["skills"]:
#             return False
#     return True
