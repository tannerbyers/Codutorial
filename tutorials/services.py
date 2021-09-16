import logging
import requests
import logging
import re
import markdown
import json 

params = {
    "state": "open",
}
headers = {'Authorization': 'token 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'}

logger = logging.getLogger(__name__)

def get_tutorial(self):
    owner = "tannerbyers"
    repo = "sample-tutorial"

    queryGithubBranchUrl = f"https://api.github.com/repos/{owner}/{repo}/branches"

    response = requests.get(queryGithubBranchUrl,
                            headers=headers, params=params)

    # TODO: Have this search through branches and find main/master
    # OR have the user send the branch they want to use in the request
    branch = response.json()[0]['name']

    queryGithubCommitUrl = f"https://api.github.com/repos/{owner}/{repo}/commits?sha={branch}"

    responseCommits = requests.get(
        queryGithubCommitUrl, headers=headers, params=params)
    allCommitsForBranch = responseCommits.json()
    allChanges = []
    commitSHAs = []

    # Note: ResponseCommits are ordered most recent to oldest (meaning first in list is most recent)
    i = len(allCommitsForBranch) - 1
    while i >= 0:
        commitSHAs.append(allCommitsForBranch[i]["sha"])
        if (i == len(allCommitsForBranch)-1):
            queryGithubDiffUrl = f"https://api.github.com/repos/{owner}/{repo}/commits/{commitSHAs[0]}"
            responsePatches = requests.get(
                queryGithubDiffUrl, headers=headers, params=params).json()
        else:
            # compare/base...head
            queryGithubDiffUrl = f"https://api.github.com/repos/{owner}/{repo}/compare/{commitSHAs[len(commitSHAs)-2]}...{commitSHAs[len(commitSHAs)-1]}"
            responsePatches = requests.get(
                queryGithubDiffUrl, headers=headers, params=params).json()
        # This is to keep track of file count without readme
        fileCounter = 0
        for file in responsePatches["files"]:
            parsedPatch = re.sub("(@@).*(@@)", "", file["patch"])
            if (parsedPatch[-1] != "\n"):
                parsedPatch += "\n"
            if (file["filename"] == "README.md"):
                parsedPatch = re.findall(
                    "(?<=\+)(.*?)(?=\n)", parsedPatch)
                parsedPatch = '\n'.join(parsedPatch)
                # Convert readme markdown to HTML
                file["parsedPatch"] = markdown.markdown(parsedPatch)
            else:
                fileCounter += 1
                file["parsedPatch"] = parsedPatch
                file["newFormat"] = getChangesInPatch(file)
                file["order"] = fileCounter

        allChanges.append(responsePatches["files"])
        i -= 1

    logger.debug(f"Length of changes {self.request.get_full_path()}")

    tutorial = allChanges
    return tutorial


def getChangesInPatch(file):
    newPatchFormat = []
    patchArray = file["parsedPatch"].splitlines()
    for line in patchArray:
        #print(line)
        lineObject = {}
        if line:
            if line[0] == "+":
                lineObject["code"] = line[1:]
                lineObject["change"] = "is-added"
            elif line[0] == "-":
                lineObject["code"] = line[1:]
                lineObject["change"] = "is-removed"
            else:
                lineObject["code"] = line
                lineObject["change"] = "None"
        newPatchFormat.append(lineObject)
    return newPatchFormat