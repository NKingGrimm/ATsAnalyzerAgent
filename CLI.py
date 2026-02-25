import subprocess
import os

RESUME_PATH = "assets/resume.txt"
JOB_POSITION_PATH = "assets/job_position.txt"
ASSETS_PATH = "assets/"


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
    input("╚ ENTER ANY KEY TO CONTINUE: ")
    _clear_screen()

def confirmResumeExists():
  # Check if the file exists
  if not os.path.exists(RESUME_PATH):
    os.makedirs(ASSETS_PATH, exist_ok=True)
    #Create file but don't write anything
    with open(RESUME_PATH, "w") as f:
      pass
    input("╔═══════════════════════════════════════════════════════════╗\n" \
          "║ IT APPEARS YOU DON'T HAVE A RESUME. A WINDOW WILL OPEN,   ║\n" \
          "║ PLEASE WRITE YOUR RESUME TO CONTINUE.                     ║\n" \
          "╠═══════════════════════════════════════════════════════════╝\n" \
          "╚ ENTER ANY KEY TO CONTINUE: ")
    # Python script waits here until Notepad is closed
    process = subprocess.Popen(['notepad.exe', RESUME_PATH])
    process.wait()
  return _check_there_are_contents(RESUME_PATH)

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
          "╚ ENTER ANY KEY TO CONTINUE: ")
    # Python script waits here until Notepad is closed
    process = subprocess.Popen(['notepad.exe', JOB_POSITION_PATH])
    process.wait()
  return _check_there_are_contents(JOB_POSITION_PATH)

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
  pass

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
  with open(fileToCheck, "r") as f:
      if not f.read(1):
          thereAreContents = False
      else:
          thereAreContents = True
  if thereAreContents is False : os.remove(fileToCheck)
  return thereAreContents