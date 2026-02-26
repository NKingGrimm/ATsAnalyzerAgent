import re
import requests

def verify_github_link_validity(gitHubLink: str):
  gitHubPattern = re.compile(r'^(?:https?://)?github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+/?$')

  if(gitHubPattern.match(gitHubLink)):
    return True
  else:
    return False

def retrieve_github_information(gitHubReposLinks: set[str]):
  returnSet = set()
  for repoLink in gitHubReposLinks:
    gitHubApiUrl = "https://raw.githubusercontent.com" + repoLink.replace("https://","").replace("github.com","") + "/main/README.md"
    try:
      response = requests.get(gitHubApiUrl)
      if response.status_code == 200:
        returnSet.add(gitHubApiUrl)
    except:
      pass
  return returnSet
