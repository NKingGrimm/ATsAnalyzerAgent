from ats_scorer import *
from CLI import *

def mainCLI():
    printWelcomeMessage()
    while(True):
        existsJobPostulation = False
        #Check the necessary material exists
        existsResume = confirmResumeExists()
        if(existsResume):
            existsJobPostulation = confirmJobPostulationExists()

        if(existsResume and existsJobPostulation):
            #Print menu
            printOptionsCLI()
            option = input(">>> ENTER YOUR CHOICE: ")
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
                    input(f"\n{Color.YELLOW}>>> PLEASE SELECT A VALID OPTION, PRESS ENTER TO CONTINUE{Color.END}")
        else:
            input(f"\n{Color.YELLOW}>>> {"RESUME" if not existsResume else "JOB POSITION"} WAS NOT LOADED. "\
                f"THE PROGRAM WILL TERMINATE,\nTHANK YOU FOR USING ATS SCORER.{Color.END}")
            break


if __name__ == "__main__":

    mainCLI()