import re
import requests
import json

def verify_github_link_validity(gitHubLink: str):
  gitHubPattern = re.compile(r'^(?:https?://)?github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+/?$')

  if(gitHubPattern.match(gitHubLink)):
    return True
  else:
    return False

def retrieve_github_api_links(gitHubReposLinks: list[str]):
  if(len(gitHubReposLinks) > 0):
    tempSet = set()
    tempDict = dict()
    # The two separated replace instructions is because "https://" might be in the link or not
    for link in gitHubReposLinks:
      tempSet.add(link.replace("https://","").replace("github.com",""))

    for repoLink in tempSet:
      gitHubApiUrl = "https://api.github.com/repos" + repoLink
      try:
        response = requests.get(gitHubApiUrl)
        if response.status_code == 200:
          # Each repository might have a different default branch
          tempDict[gitHubApiUrl] = response.json()['default_branch']
      except:
        return None, f"AN ERROR OCURRED WITH {gitHubApiUrl}"

    for apiLink in tempDict:
      gitHubRepoContentsUrl = apiLink + "/contents/"
      try:
        response = requests.get(gitHubRepoContentsUrl)
        if response.status_code == 200:
          for data in response.json():
            if("README" in str(data['name']).upper()):
              tempDict[apiLink] = (tempDict[apiLink], data['name'])
              break
      except:
        return None, f"AN ERROR OCURRED WITH {gitHubRepoContentsUrl}"

  return tempDict, None

def get_github_readme_text(repository: str, defaultMainBranch: str, readmeFileName: str):
  repository = repository.replace("https://api.github.com/repos", "https://raw.githubusercontent.com") + f"/{defaultMainBranch}/{readmeFileName}"
  try:
    response = requests.get(repository)
    if response.status_code == 200:
      return response.text, None
  except:
    return None, f"AN ERROR OCURRED WITH {repository}"
