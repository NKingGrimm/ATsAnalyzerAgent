from ats_scorer import *
from CLI import *

def mainCLI():
    printWelcomeMessage()
    existsResume = False
    while(existsResume is False):
        existsResume = confirmResumeExists()
    existsJobPostulation = False
    while(existsJobPostulation is False):
        existsJobPostulation = confirmJobPostulationExists()
    while(True):
        printOptionsCLI()
        option = input("╠ ENTER YOUR OPTION: ")
        match option:
            case "1":
                run_ats_analyzer()
            case "2":
                add_another_job_position()
            case "3":
                add_personal_project()
            case "4":
                rewrite_resume()
            case "5":
                edit_resume()
            case "6":
                break
            case _:
                input("╚ PLEASE SELECT A VALID OPTION, PRESS ENTER ANY KEY TO CONTINUE ")

if __name__ == "__main__":

    mainCLI()

    # with open("job.txt", "r", encoding="utf-8") as f:
    #     job_description = f.read()

    # with open("resume.txt", "r", encoding="utf-8") as f:
    #     resume_description = f.read()

    # extractedFacts = fact_extraction_from_resume(resume_description)
    # result = score_resume_against_job(job_description, resume_description)
    # action = decide_action(result.overall_score)
    # if action == "REWRITE_RESUME":
    #     rewriteContent = rewrite_resume(resume_description,
    #                                     job_description,
    #                                     extractedFacts.model_dump(),
    #                                     result.weak_areas,
    #                                     result.missing_required_skills)
    #     print(rewriteContent, end='\n')