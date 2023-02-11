import json
from collections import defaultdict
import copy
from getQuestionFromLC import getAllQuestions

setlist= "blind75"
problemNames = open(f"problemSetInfo/{setlist}problems.txt", "r")
problemTopics = open(f"problemSetInfo/{setlist}Topics.txt", "r")
probList = problemNames.read().split("\n")
topicList = problemTopics.read().split("\n")
topics = {}
problemTopic = {}


i = 0
for b in topicList:
    topics[b] = []
    while i < len(probList) and probList[i] != "":
        topics[b].append(probList[i])
        problemTopic[probList[i].lower()] = b
        i += 1
    i += 1

problemInfo = defaultdict(lambda: [])
setlistProblems = {"IDs": []}
probsFound = set()
allQuestions = getAllQuestions()
for problem in problemTopic:  # purposefully inefficient to preserve order, not really that important to optimize
    isFound = False
    for i, q in enumerate(allQuestions):

        if q["title"].lower() == problem.lower():
            newProblem = {}
            newProblem["TITLE"] = q["title"]
            newProblem["URL"] = "https://leetcode.com/problems/" + q["titleSlug"]
            newProblem["DIFFICULTY"] = q["difficulty"]
            setlistProblems["IDs"].append({i + 1: copy.deepcopy(newProblem)})
            newProblem["ID"] = i + 1

            topic = problemTopic[q["title"].lower()]
            problemInfo[topic].append(newProblem)
            isFound = True
    if not isFound:
        print("NOT FOUND: ", problem)

with open(f"problemSetInfo/{setlist}problems.json", "w") as writeFile:
    json.dump(problemInfo, writeFile)

if setlist == "neetcode150":
    with open(f"problemSetInfo/setlistProblemIDs.json", "w") as writeFile:
        json.dump(setlistProblems, writeFile)
elif setlist == "blind75":
    print(probList)
    with open("problemSetInfo/setlistProblemIDs.json", "r") as readFile:
        problemIDs = json.load(readFile)
    for p in problemIDs["IDs"]:
        p = p[tuple(p.keys())[0]]
        print(p["TITLE"])
        if p["TITLE"] in probList:
            p["INBLIND75"] = True
        else:
            p["INBLIND75"] = False
    with open(f"problemSetInfo/setlistProblemIDs.json", "w") as writeFile:
        json.dump(problemIDs, writeFile)

