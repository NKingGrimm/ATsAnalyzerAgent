import os
import subprocess
import json

ASSETS_PATH = "assets/"
RESUME_PATH = ASSETS_PATH + "resume.txt"
JOB_POSITION_PATH = ASSETS_PATH + "job_position.txt"
GITHUB_REPOS_PATH = ASSETS_PATH + "github_repos.json"

def check_file_exists(fileToCheck) -> bool:
  if fileToCheck == "RESUME":
    return _utility_check_file_exists(RESUME_PATH)
  elif fileToCheck == "JOB_POSITION":
    return _utility_check_file_exists(JOB_POSITION_PATH)
  elif fileToCheck == "GITHUB_REPOS":
    return _utility_check_file_exists(GITHUB_REPOS_PATH)

def edit_stored_resume():
  _utility_edit_file(RESUME_PATH)

def create_file(fileToCreate: str):
  if fileToCreate == "RESUME":
    _utility_create_file(RESUME_PATH)
    edit_stored_resume()
  elif fileToCreate == "JOB_POSITION":
    _utility_create_file(JOB_POSITION_PATH)
    _utility_edit_file(JOB_POSITION_PATH)
  elif fileToCreate == "GITHUB_REPOS":
    _utility_create_file(GITHUB_REPOS_PATH)

def check_there_are_file_contents(fileToCheck):
  if fileToCheck == "RESUME":
    return _utility_confirm_contents_existance(RESUME_PATH)
  elif fileToCheck == "JOB_POSITION":
    return _utility_confirm_contents_existance(JOB_POSITION_PATH)

def delete_file(fileToDelete: str):
  if fileToDelete == "RESUME":
    _utility_delete_file(RESUME_PATH)
  elif fileToDelete == "JOB_POSITION":
    _utility_delete_file(JOB_POSITION_PATH)

def get_file_contents(fileToRead: str) -> str:
  if fileToRead == "RESUME":
    f = open(RESUME_PATH, "r", encoding="utf-8")
  elif fileToRead == "JOB_POSITION":
    f = open(JOB_POSITION_PATH, "r", encoding="utf-8")
  elif fileToRead == "GITHUB_REPOS":
    f = open(GITHUB_REPOS_PATH, "r", encoding="utf-8")
  else:
    return ""
  return f.read()

def add_repo_info_to_storage(reposDict: dict):
  if(reposDict):
      with open(GITHUB_REPOS_PATH, "w", encoding="UTF-8") as f:
        f.write(json.dumps(reposDict, indent=2))

def get_repo_info_from_storage() -> dict:
  return json.loads(get_file_contents("GITHUB_REPOS"))

"""
============================= UTILITY FUNCTIONS ========================================
"""

def _utility_confirm_contents_existance(fileToCheck: str) -> bool:
  with open(fileToCheck, "r", encoding="UTF-8", errors='replace') as f:
      if not f.read(1):
          return False
  return True

def _utility_delete_file(fileToDelete: str):
  os.remove(fileToDelete)

def _utility_create_file(fileToCreate: str):
  os.makedirs(ASSETS_PATH, exist_ok = True)
  with open(fileToCreate, "w") as f:
    pass

def _utility_check_file_exists(filePath: str) -> bool:
  return os.path.exists(filePath)

def _utility_edit_file(fileToEdit: str):
  #It will open `fileToEdit` on notepad, change as you need
  process = subprocess.Popen(['notepad.exe', fileToEdit])
  process.wait()
