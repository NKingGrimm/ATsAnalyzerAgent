from ats_scorer import *

with open("job.txt", "r", encoding="utf-8") as f:
    job_description = f.read()

with open("resume.txt", "r", encoding="utf-8") as f:
    resume_description = f.read()

fact_extraction_from_resume(resume_description)
result = score_resume_against_job(job_description)
action = decide_action(result.overall_score)
# if action is "REWRITE_RESUME":
#     rewrite_resume()

print(f"ATS Score: {result.overall_score}%")
print(f"Action: {action}")
print("Missing skills:", result.missing_required_skills)
print("Weak Areas:", result.weak_areas)
print("Strong Matches:", result.strong_matches)
print("Risk Flags:", result.risk_flags)
print("Summary:", result.summary)