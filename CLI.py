import subprocess
import textwrap
import json
from typing import List

from ats_scorer import (analyze_resume_and_get_score,
                        get_project_summary_and_keywords,
                        get_rewritten_sections)

from github_handler import  (verify_github_link_validity,
                            retrieve_github_api_links)
from storage import (check_file_exists,
                    create_file,
                    check_there_are_file_contents,
                    delete_file,
                    add_repo_info_to_storage,
                    get_repo_info_from_storage,
                    edit_stored_resume,
                    get_file_contents)

weakAreas = []
missingSkills = []

class Color:
  PURPLE    = '\033[1;35;48m'
  CYAN      = '\033[1;36;48m'
  BOLD      = '\033[1;37;48m'
  BLUE      = '\033[1;34;48m'
  GREEN     = '\033[1;32;48m'
  YELLOW    = '\033[1;33;48m'
  RED       = '\033[1;31;48m'
  BLACK     = '\033[1;30;48m'
  UNDERLINE = '\033[4;37;48m'
  END       = '\033[1;37;0m' # Reset code is important

CORNERS = 2
BOX_LENGTH = 78
""" The text box lenght has one space on each side
    before it touches the box length """
TEXT_BOX_LENGTH = BOX_LENGTH - 2
COLOR_SEQUENCE_LEN = len(Color.END)
VALID_YES = {"Y", "y", "yes", "YES", "Yes"}
VALID_NO = {"N", "n", "no", "NO", "No"}
VALID_YES_NO = VALID_YES | VALID_NO

def printWelcomeMessage():
    _utility_clear_screen()
    input("╔══════════════════════════════════════════════════════════════════════════════════╗\n"\
          '║ __     __     ______     __         ______     ______     __    __     ______    ║\n'\
          '║/\ \  _ \ \   /\  ___\   /\ \       /\  ___\   /\  __ \   /\ "-./  \   /\  ___\   ║\n'\
          '║\ \ \/ ".\ \  \ \  __\   \ \ \____  \ \ \____  \ \ \/\ \  \ \ \-./\ \  \ \  __\   ║\n'\
          '║ \ \__/".~\_\  \ \_____\  \ \_____\  \ \_____\  \ \_____\  \ \_\ \ \_\  \ \_____\ ║\n'\
          '║  \/_/   \/_/   \/_____/   \/_____/   \/_____/   \/_____/   \/_/  \/_/   \/_____/ ║\n'\
          "╠══════════════════════════════════════════════════════════════════════════════════╣\n"\
          "║ THIS PROGRAM IS INTENDED TO HELP YOU ANALYZE A GIVEN RESUME AGAINST A JOB        ║\n"\
          "║ POSITION USING AI. YOU CAN GET THE ATS SCORE, ADD PERSONAL PROJECT EXPERIENCE    ║\n"\
          "║ AND REWRITE YOUR RESUME TO INCREASE YOUR ATS SCORE.                              ║\n"\
          "╚══════════════════════════════════════════════════════════════════════════════════╝\n"\
          ">>> PRESS ENTER TO CONTINUE: ")
    _utility_clear_screen()

def printOptionsCLI():
    _utility_clear_screen()
    print(f"╔{"═"*BOX_LENGTH}╗")
    _utility_print_message('SELECT ONE OF THE FOLLOWING OPTIONS:', False)
    _utility_print_message('  1. OBTAIN ATS SCORE AND ANALYSIS', False)
    _utility_print_message('  2. ADD ANOTHER JOB POSITION', False)
    _utility_print_message('  3. ADD PERSONAL PROJECT', False)
    _utility_print_message('  4. EDIT ORIGINAL RESUME', False)
    _utility_print_message('  5. REWRITE RESUME', False)
    _utility_print_message('  6. WRITE A COVER LETTER', False)
    _utility_print_message('  7. EXIT', False)
    print(f"╚{"═"*BOX_LENGTH}╝")

def confirmResumeExists():
  resumeExists = check_file_exists("RESUME")
  if not resumeExists:
    _utility_print_warning( "IT APPEARS YOU DON'T HAVE A RESUME. A WINDOW " \
                            "WILL OPEN, PLEASE WRITE YOUR RESUME TO CONTINUE.")
    continueWithRequest = _utility_get_yes_no_input(f"{Color.YELLOW}>>> DO YOU WISH TO CONTINUE? (Y|N): {Color.END}")
    if continueWithRequest in VALID_YES:
      create_file("RESUME")
      resumeHasContents = check_there_are_file_contents("RESUME")
      if not resumeHasContents:
        _utility_print_error("THE RESUME FILE DOESN'T HAVE ANY CONTENTS")
        delete_file("RESUME")
        return False
    else:
      return False

  return True

def confirmJobPostulationExists():
  jobPositionExists = check_file_exists("JOB_POSITION")
  if not jobPositionExists:
    _utility_print_warning( "IT APPEARS YOU DON'T HAVE A JOB POSITION. " \
                            "A WINDOW WILL OPEN, PLEASE COPY A JOB " \
                            "POSITION TO CONTINUE.")
    continueWithRequest = _utility_get_yes_no_input(f"{Color.YELLOW}>>> DO YOU WISH TO CONTINUE? (Y|N): {Color.END}")
    if continueWithRequest in VALID_YES:
      create_file("JOB_POSITION")
      jobPositionHasContents = check_there_are_file_contents("JOB_POSITION")
      if not jobPositionHasContents:
        _utility_print_error("THE JOB POSITION FILE DOESN'T HAVE ANY CONTENTS")
        delete_file("JOB_POSITION")
        return False
    else:
      return False

  return True

def run_ats_analyzer():
  global weakAreas
  global missingSkills

  colorSequenceLen = len(Color.BLUE) + len(Color.END)
  try:
    analysisResult, action = analyze_resume_and_get_score()
  except Exception as e:
    _utility_print_error("FAILED TO RUN ATS ANALYSIS: " + str(e))
    input(">>> PRESS ENTER TO CONTINUE")
    return

  if(action == "APPLY_AS_IS"):
    coloredAction = f"{Color.GREEN + action+ Color.END}"
  elif(action == "REWRITE_RESUME"):
    coloredAction = f"{Color.YELLOW+ action+ Color.END}"
  elif(action == "SKIP"):
    coloredAction = f"{Color.RED+ action+ Color.END}"

  print(f"╔{"═"*BOX_LENGTH}╗")
  _utility_print_message(f"{Color.BLUE}ATS SCORE{Color.END}: " + str(analysisResult.overall_score), False, colorSequenceLen)
  _utility_print_message(f"{Color.BLUE}STRONG MATCHES:{Color.END}", False, colorSequenceLen)
  for match in analysisResult.strong_matches: _utility_print_message(match, False)
  _utility_print_message(f"{Color.BLUE}WEAK AREAS:{Color.END}", False, colorSequenceLen)
  for area in analysisResult.weak_areas: _utility_print_message(area, False)
  _utility_print_message(f"{Color.BLUE}MISSING REQUIRED SKILLS:{Color.END}", False, colorSequenceLen)
  for skill in analysisResult.missing_required_skills: _utility_print_message(skill, False)
  _utility_print_message(f"{Color.BLUE}SUMMARY:{Color.END}", False, colorSequenceLen)
  _utility_print_message(analysisResult.summary, False)
  _utility_print_message(f"{Color.BLUE}ACTION: {Color.END}" + coloredAction, False, (2*colorSequenceLen))
  print(f"╚{"═"*BOX_LENGTH}╝")

  # Set these variables in order to rewrite the resume
  weakAreas = analysisResult.weak_areas
  missingSkills = analysisResult.missing_required_skills

  input(">>> PRESS ENTER TO CONTINUE")

def add_another_job_position():
  _utility_print_warning("ALL CONTENTS IN THE CURRENT POSITION WILL BE DELETED")
  deleteCurrentJob = _utility_get_yes_no_input(f"{Color.YELLOW}>>> DO YOU WISH TO CONTINUE? (Y|N): {Color.END}")
  if deleteCurrentJob in VALID_YES:
    try:
      global weakAreas
      global missingSkills
      delete_file("JOB_POSITION")
      # Clear these variables to avoid resume rewrite operation with obselete information
      weakAreas = []
      missingSkills = []
    except FileNotFoundError:
      pass
    except PermissionError:
      _utility_print_error("PERMISSION DENIED TO DELETE, THE FILE MIGHT BE IN USE.")
    except OSError as e:
      _utility_print_error("AN UNEXPECTED OS ERROR OCCURRED: " + str(e))

def add_personal_project():
  _utility_print_message( "TO ADD A PERSONAL PROJECT YOU HAVE TO PROVIDE A PUBLIC GITHUB " \
                          "REPOSITORY LINK WITH A README FILE. AN AI AGENT WILL EXTRACT A " \
                          "SUMMARY AND A LIST OF KEYWORDS TO BE USED IN CASE YOU WANT TO " \
                          "REWRITE YOUR RESUME TO INCREASE YOUR ATS SCORE FOR A GIVEN " \
                          "POSITION", True)
  continueWithRequest = _utility_get_yes_no_input(">>> DO YOU WISH TO CONTINUE? (Y|N): ")

  if continueWithRequest in VALID_YES:
    githubLink = "NOT EMPTY"
    gitHubLinksCollection = list()
    _utility_print_message( "ADD YOUR GITHUB LINK, NOTE THAT IT SHOULD HAVE A FORMAT AS " \
                            "FOLLOWS: (https://)github.com/user/repository", True)

    # Retrieve all links and check if the syntax is correct, break if an empty line is entered
    while(githubLink != ""):
      githubLink = input(">>> ENTER YOUR REPO LINK (ENTER AN EMPTY LINE TO FINISH): ")
      linkIsValid = verify_github_link_validity(githubLink)
      if githubLink == "":
        break
      if linkIsValid:
        gitHubLinksCollection.append(githubLink)
      else:
        _utility_print_warning("LINK INVALID")

    if(len(gitHubLinksCollection) > 0):
      gitHubValidContentLinks, error = retrieve_github_api_links(gitHubLinksCollection)
      if error:
        _utility_print_error(error)
        input(f"{Color.RED}>>> PRESS ENTER TO CONTINUE{Color.END}")
        return

      reposInfoJSON = dict()
      reposFileExists = check_file_exists("GITHUB_REPOS")
      if(reposFileExists):
        try:
          reposInfoJSON = get_repo_info_from_storage()
        except json.decoder.JSONDecodeError as e:
          _utility_print_error("THE REPOSITORY COLLECTION FILE IS MALFORMED: " + str(e))
          input(f"{Color.RED}>>> PRESS ENTER TO CONTINUE{Color.END}")
          return
      else:
        create_file("GITHUB_REPOS")

      for repo in gitHubValidContentLinks:
        # It only has a tuple type when retrieve_github_api_links found a default branch
        # AND a README file, otherwise the type will be just string with the found default
        # branch
        if isinstance(gitHubValidContentLinks[repo], tuple):
          defaultRepoBranch = gitHubValidContentLinks[repo][0]
          readmeFileName = gitHubValidContentLinks[repo][1]
          try:
            projectSummary = get_project_summary_and_keywords(repo, defaultRepoBranch, readmeFileName)
          except RuntimeError as e:
            _utility_print_error(str(e))
            continue
          # If there is a valid summary
          if(projectSummary.summary):
            repoName = repo.replace("https://api.github.com/repos/", "")
            reposInfoJSON[repoName] = {**projectSummary.model_dump()}
        else:
          _utility_print_warning("REPO "+repo+" DOESN'T HAVE A README FILE.")

      add_repo_info_to_storage(reposInfoJSON)
    else:
      _utility_print_warning("NO LINKS WERE ADDED")
  input(">>> PRESS ENTER TO CONTINUE")

def edit_resume():
  resumeExists = check_file_exists("RESUME")
  if(resumeExists):
    global weakAreas
    global missingSkills
    _utility_print_warning("A WINDOW WITH YOUR RESUME WILL POP OPEN, SAVE AND CLOSE IT.")
    input(f"{Color.YELLOW}>>>PRESS ENTER TO CONTINUE: {Color.END}")
    edit_stored_resume()
    # Clear these variables to avoid resume rewrite operation with obselete information
    weakAreas = []
    missingSkills = []
  else:
    _utility_print_warning("YOU DON'T HAVE A RESUME TO EDIT.")

def rewrite_resume():
  global weakAreas
  global missingSkills

  if weakAreas and missingSkills:
    resume_description = get_file_contents("RESUME")
    job_description = get_file_contents("JOB_POSITION")
    repos = get_repo_info_from_storage()
    githubProjectsStr = ""
    for repo in repos:
      githubProjectsStr += f"Repo name: {repo}, Summary: ({repos[repo]["summary"]}), Keywords: [{repos[repo]["keywords"]}]\n"
    rewrittenSections = get_rewritten_sections(resume_description, job_description, githubProjectsStr, weakAreas, missingSkills)

    print(f"╔{"═"*BOX_LENGTH}╗")
    _utility_print_message("CHANGE THIS SECTIONS IN YOUR RESUME MANUALLY: ", False)
    _utility_print_message(f"SUMMARY: {rewrittenSections.summary}", False)

    _utility_print_message(f"NEW HARD SKILLS:", False)
    for skill in rewrittenSections.hard_skills:
      _utility_print_message(skill, False)

    _utility_print_message(f"PROJECTS:", False)
    for project in rewrittenSections.projects:
      _utility_print_message(project, False)
      for bullet in rewrittenSections.projects[project]:
        _utility_print_message(bullet, False)
    print(f"╚{"═"*BOX_LENGTH}╝")
  else:
    _utility_print_warning("YOU HAVE TO RUN ATS ANALYZER FIRST")
  input(">>> PRESS ENTER TO CONTINUE")

def write_cover_letter():
  pass

"""
============================= UTILITY FUNCTIONS ========================================
"""

def _utility_print_warning(warningToPrint: str):
  print(f"{Color.YELLOW}",end='')
  _utility_print_message(warningToPrint, True)
  print(f"{Color.END}", end='')

def _utility_print_error(errorToPrint: str):
  print(f"{Color.RED}", end='')
  _utility_print_message(errorToPrint, True)
  print(f"{Color.END}", end='')

def _utility_print_message(textToPrint: str, printUpperAndLowerLimits: bool, additionalLength: int = 0):
  wrappedText = _utility_wrap_text(textToPrint)
  TEXT_LENGTH = TEXT_BOX_LENGTH + additionalLength

  if printUpperAndLowerLimits : print(f"╔{'═'*(BOX_LENGTH)}╗")
  for textLine in wrappedText:
    print("║", str(textLine).ljust(TEXT_LENGTH), "║")
  if printUpperAndLowerLimits : print(f"╚{'═'*(BOX_LENGTH)}╝")

def _utility_wrap_text(textToWrap: str) -> list[str]:
  return textwrap.wrap(textToWrap, width=TEXT_BOX_LENGTH)

def _utility_clear_screen():
    subprocess.run("cls", shell=True, check=False)

def _utility_get_yes_no_input(message: str) -> str:
  answer = ""
  while answer not in VALID_YES_NO:
    answer = input(message)
  return answer

def _utility_print_analysis_text_wrapped(analysisCategory: str, analysisStrLis: List[str]):
  print(f"║ {(analysisCategory + ": ").ljust(58)}║")
  for match in analysisStrLis:
    wrappedLines = textwrap.wrap(match, width=56)
    for wrappedLine in wrappedLines:
        if wrappedLine == wrappedLines[0]:
          print("║ -", wrappedLine.ljust(55), "║")
        else:
          print("║  ", wrappedLine.ljust(55), "║")
