from ats_scorer import *

with open("job.txt", "r", encoding="utf-8") as f:
    job_description = f.read()

with open("resume.txt", "r", encoding="utf-8") as f:
    resume_description = f.read()

extractedFacts = fact_extraction_from_resume(resume_description)
result = score_resume_against_job(job_description, resume_description)
action = decide_action(result.overall_score)
if action == "REWRITE_RESUME":
    rewriteContent = rewrite_resume(resume_description,
                                    job_description,
                                    extractedFacts.model_dump(),
                                    result.weak_areas,
                                    result.missing_required_skills)
    print(rewriteContent, end='\n')

