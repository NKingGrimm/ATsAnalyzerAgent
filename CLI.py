import subprocess
import os
from ats_scorer import *
import textwrap
from typing import List

class Color:
    PURPLE = '\033[1;35;48m'
    CYAN = '\033[1;36;48m'
    BOLD = '\033[1;37;48m'
    BLUE = '\033[1;34;48m'
    GREEN = '\033[1;32;48m'
    YELLOW = '\033[1;33;48m'
    RED = '\033[1;31;48m'
    BLACK = '\033[1;30;48m'
    UNDERLINE = '\033[4;37;48m'
    END = '\033[1;37;0m' # Reset code is important

def printWelcomeMessage():
    _clear_screen()
    print("╔══════════════════════════════════════════════════════════════════════════════════╗\n"\
          '║ __     __     ______     __         ______     ______     __    __     ______    ║\n'\
          '║/\ \  _ \ \   /\  ___\   /\ \       /\  ___\   /\  __ \   /\ "-./  \   /\  ___\   ║\n'\
          '║\ \ \/ ".\ \  \ \  __\   \ \ \____  \ \ \____  \ \ \/\ \  \ \ \-./\ \  \ \  __\   ║\n'\
          '║ \ \__/".~\_\  \ \_____\  \ \_____\  \ \_____\  \ \_____\  \ \_\ \ \_\  \ \_____\ ║\n'\
          '║  \/_/   \/_/   \/_____/   \/_____/   \/_____/   \/_____/   \/_/  \/_/   \/_____/ ║\n'\
          "╠══════════════════════════════════════════════════════════════════════════════════╣\n"\
          "║ THIS PROGRAM IS INTENDED TO HELP YOU ANALYZE A GIVEN RESUME AGAINST A JOB        ║\n"\
          "║ POSITION USING AI. YOU CAN GET THE ATS SCORE, ADD PERSONAL PROJECT EXPERIENCE    ║\n"\
          "║ AND REWRITE YOUR RESUME TO INCREASE YOUR ATS SCORE.                              ║\n"\
          "╠══════════════════════════════════════════════════════════════════════════════════╝")
    input("╚ PRESS ENTER TO CONTINUE: ")
    _clear_screen()

def confirmResumeExists():
  # Check if the file exists
  if not os.path.exists(RESUME_PATH):
    #Create assets directory but don't throw error if it already exists
    os.makedirs(ASSETS_PATH, exist_ok = True)
    #Create file but don't write anything
    with open(RESUME_PATH, "w") as f:
      pass
    input("╔═══════════════════════════════════════════════════════════╗\n" \
          "║ IT APPEARS YOU DON'T HAVE A RESUME. A WINDOW WILL OPEN,   ║\n" \
          "║ PLEASE WRITE YOUR RESUME TO CONTINUE.                     ║\n" \
          "╠═══════════════════════════════════════════════════════════╝\n" \
          "╚ PRESS ENTER TO CONTINUE: ")
    # Python script waits here until Notepad is closed
    process = subprocess.Popen(['notepad.exe', RESUME_PATH])
    process.wait()
  try:
    return _check_there_are_contents(RESUME_PATH)
  except UnicodeDecodeError:
    print(f"{Color.RED}" \
          "╔═══════════════════════════════════════════════════════════╗\n" \
          "║ THE RESUME TEXT IS NOT ENCODED AS UTF-8                   ║\n" \
          "╚═══════════════════════════════════════════════════════════╝" \
          f"{Color.END}")
    os.remove(RESUME_PATH)
    return False

def confirmJobPostulationExists():
  # Check if the file exists
  if not os.path.exists(JOB_POSITION_PATH):
    #Create file but don't write anything
    with open(JOB_POSITION_PATH, "w") as f:
      pass
    input("╔═══════════════════════════════════════════════════════════╗\n" \
          "║ IT APPEARS YOU DON'T HAVE A JOB POSITION.                 ║\n" \
          "║ A WINDOW WILL OPEN, PLEASE COPY A JOB POSITION TO         ║\n" \
          "║ CONTINUE.                                                 ║\n" \
          "╠═══════════════════════════════════════════════════════════╝\n" \
          "╚ PRESS ENTER TO CONTINUE: ")
    # Python script waits here until Notepad is closed
    process = subprocess.Popen(['notepad.exe', JOB_POSITION_PATH])
    process.wait()
  try:
    return _check_there_are_contents(JOB_POSITION_PATH)
  except UnicodeDecodeError:
    print(f"{Color.RED}" \
          "╔═══════════════════════════════════════════════════════════╗\n" \
          "║ THE JOB POSITION TEXT IS NOT ENCODED AS UTF-8             ║\n" \
          "╚═══════════════════════════════════════════════════════════╝" \
          f"{Color.END}")
    os.remove(JOB_POSITION_PATH)
    return False

def printOptionsCLI():
    _clear_screen()
    print("╔═══════════════════════════════════════════════════════════╗\n" \
          "║ SELECT ONE OF THE FOLLOWING OPTIONS:                      ║\n" \
          "║   1. OBTAIN ATS SCORE AND ANALYSIS                        ║\n" \
          "║   2. ADD ANOTHER JOB POSITION                             ║\n" \
          "║   3. ADD PERSONAL PROJECT                                 ║\n" \
          "║   4. REWRITE RESUME                                       ║\n" \
          "║   5. EDIT ORIGINAL RESUME                                 ║\n" \
          "║   6. EXIT                                                 ║\n" \
          "╠═══════════════════════════════════════════════════════════╝")

def run_ats_analyzer():
  analysisResult, action = analyze_resume_and_get_score()

  print( "╠═══════════════════════════════════════════════════════════╗\n" \
        f"║{(' ATS SCORE: '+ str(analysisResult.overall_score)).ljust(59)}║")
  _print_analysis_text_wrapped("STRONG MATCHES", analysisResult.strong_matches)
  _print_analysis_text_wrapped("WEAK AREAS", analysisResult.weak_areas)
  _print_analysis_text_wrapped("MISSING REQUIRED SKILLS", analysisResult.missing_required_skills)
  print( "║ SUMMARY:                                                  ║")
  wrappedLines = textwrap.wrap(analysisResult.summary, width=57)
  for line in wrappedLines:
    print('║', line.ljust(57), '║')
  print(f"║{' '*59}║\n"\
        f"║{(" ACTION: " + action).ljust(59)}║\n" \
          "╠═══════════════════════════════════════════════════════════╝")

  input("╚ PRESS ENTER TO CONTINUE")

def add_another_job_position():
  pass

def add_personal_project():
  pass

def rewrite_resume():
  pass

def edit_resume():
  pass

def _clear_screen():
    # Check the operating system name
    if os.name == 'nt':
        # Command for Windows
        subprocess.run(['cls'], shell=True, check=True)
    else:
        # Command for Linux/macOS (posix is the name for non-Windows)
        subprocess.run(['clear'], check=True)

def _check_there_are_contents(fileToCheck: str):
  thereAreContents = False
  with open(fileToCheck, "r", encoding="UTF-8") as f:
      if not f.read(1):
          thereAreContents = False
      else:
          thereAreContents = True
  if thereAreContents is False : os.remove(fileToCheck)
  return thereAreContents

def _print_analysis_text_wrapped(analysisCategory: str, analysisStrLis: List[str]):
  print(f"║ {(analysisCategory + ": ").ljust(58)}║")
  for match in analysisStrLis:
    wrappedLines = textwrap.wrap(match, width=56)
    for wrappedLine in wrappedLines:
        if wrappedLine == wrappedLines[0]:
          print("║ -", wrappedLine.ljust(55), "║")
        else:
          print("║  ", wrappedLine.ljust(55), "║")
