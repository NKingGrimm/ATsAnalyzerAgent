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
        option = input("╠ ENTER YOUR CHOICE: ")
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
                input("╚ PLEASE SELECT A VALID OPTION, PRESS ENTER TO CONTINUE ")

if __name__ == "__main__":

    mainCLI()