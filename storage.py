import os
import subprocess
import json

ASSETS_PATH = "assets/"
RESUME_PATH = ASSETS_PATH + "resume.txt"
JOB_POSITION_PATH = ASSETS_PATH + "job_position.txt"
GITHUB_REPOS_PATH = ASSETS_PATH + "github_repos.json"
FILE_PATHS = {
  "RESUME": RESUME_PATH,
  "JOB_POSITION": JOB_POSITION_PATH,
  "GITHUB_REPOS": GITHUB_REPOS_PATH,
}

def _resolve_file_path(fileKey: str) -> str:
  try:
    return FILE_PATHS[fileKey]
  except KeyError as e:
    raise ValueError(f"UNKNOWN FILE KEY: {fileKey}") from e

def check_file_exists(fileToCheck) -> bool:
  return _utility_check_file_exists(_resolve_file_path(fileToCheck))

def edit_stored_resume():
  _utility_edit_file(RESUME_PATH)

def create_file(fileToCreate: str):
  targetPath = _resolve_file_path(fileToCreate)
  _utility_create_file(targetPath)
  if fileToCreate == "RESUME":
    edit_stored_resume()
  elif fileToCreate == "JOB_POSITION":
    _utility_edit_file(targetPath)

def check_there_are_file_contents(fileToCheck):
  return _utility_confirm_contents_existance(_resolve_file_path(fileToCheck))

def delete_file(fileToDelete: str):
  _utility_delete_file(_resolve_file_path(fileToDelete))

def get_file_contents(fileToRead: str) -> str:
  targetPath = _resolve_file_path(fileToRead)
  with open(targetPath, "r", encoding="utf-8") as f:
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
  with open(fileToCreate, "w", encoding="utf-8") as f:
    pass

def _utility_check_file_exists(filePath: str) -> bool:
  return os.path.exists(filePath)

def _utility_edit_file(fileToEdit: str):
  #It will open `fileToEdit` on notepad, change as you need
  process = subprocess.Popen(['notepad.exe', fileToEdit])
  process.wait()
