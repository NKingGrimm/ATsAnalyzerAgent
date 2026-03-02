import re
import requests

def verify_github_link_validity(gitHubLink: str):
  gitHubPattern = re.compile(r'^(?:https?://)?github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+/?$')

  if(gitHubPattern.match(gitHubLink)):
    return True
  else:
    return False

def retrieve_github_api_links(gitHubReposLinks: list[str]):
  if len(gitHubReposLinks) == 0:
    return {}, None

  tempSet = set()
  tempDict = {}
  # The two separated replace instructions is because "https://" might be in the link or not
  for link in gitHubReposLinks:
    tempSet.add(link.replace("https://","").replace("github.com",""))

  for repoLink in tempSet:
    gitHubApiUrl = "https://api.github.com/repos" + repoLink
    try:
      response = requests.get(gitHubApiUrl, timeout=10)
      response.raise_for_status()
      # Each repository might have a different default branch
      tempDict[gitHubApiUrl] = response.json()['default_branch']
    except (requests.RequestException, KeyError, ValueError) as e:
      return None, f"AN ERROR OCCURRED WITH {gitHubApiUrl}: {e}"

  for apiLink in list(tempDict):
    gitHubRepoContentsUrl = apiLink + "/contents/"
    try:
      response = requests.get(gitHubRepoContentsUrl, timeout=10)
      response.raise_for_status()
      for data in response.json():
        if "README" in str(data.get('name', '')).upper():
          tempDict[apiLink] = (tempDict[apiLink], data['name'])
          break
    except (requests.RequestException, KeyError, ValueError) as e:
      return None, f"AN ERROR OCCURRED WITH {gitHubRepoContentsUrl}: {e}"

  return tempDict, None

def get_github_readme_text(repository: str, defaultMainBranch: str, readmeFileName: str):
  repository = repository.replace("https://api.github.com/repos", "https://raw.githubusercontent.com") + f"/{defaultMainBranch}/{readmeFileName}"
  try:
    response = requests.get(repository, timeout=10)
    response.raise_for_status()
    return response.text, None
  except requests.RequestException as e:
    return None, f"AN ERROR OCCURRED WITH {repository}: {e}"
