import random
from getQuestionFromLC import *
from lcUtils import *
from datetime import *
import os.path
import discord
import json


# Method to check if the date has changed, if it has, it will generate a new question and send it to the channel
async def dailyQuestion(client):
    if checkNewDate():
        embed = getEmbed()
        question = getTodayQuestion()
        url = "https://leetcode.com/problems/" + question["titleSlug"]
        diff = question["difficulty"].lower()
        title = question["title"]

        embed.description = f"Today's {diff} question: {title} \n {url} \n\n if you're new, do `-help` to learn how to play"
        embed.colour = discord.Colour.blue()

        for file in os.listdir("servers"):
            with open(f"servers/{file}", "r") as readFile:
                server = json.load(readFile)
            channelId = server['LOTDCHANNEL']
            channelCtx = client.get_channel(channelId)
            if channelCtx:
                if server["LOTDPING"]:
                    await channelCtx.send(server["LOTDPING"])
                await channelCtx.send(embed=embed)

        for playerFile in os.listdir("players"):  # resets all player's "HASSOLVEDTODAY property to false
            with open(f"players/{playerFile}", "r") as readFile:
                account = json.load(readFile)
            account["HASSOLVEDTODAY"] = False
            with open(f"players/{playerFile}", "w") as writeFile:
                json.dump(account, writeFile)


def getTodayQuestion():
    with open('./questions/todayQuestion.json', 'r') as readFile:
        today = json.load(readFile)

    with open('./questions/questionsList.json', 'r') as readFile:
        questions_list = json.load(readFile)["QUESTIONS"]

    today_id = today["LASTINDEX"] + 1
    today_question = getQuestion(questions_list[today_id])

    today["LASTINDEX"] += 1
    today["TODAYDATE"] = str((datetime.utcnow() + timedelta(hours=10)).date())
    today["QUESTIONID"] = questions_list[today_id]
    today["QUESTIONNAME"] = today_question["title"]
    today["QUESTIONSLUG"] = today_question["titleSlug"]
    today["DIFFICULTY"] = today_question["difficulty"]

    with open('./questions/todayQuestion.json', 'w') as writeFile:
        json.dump(today, writeFile)

    return today_question


def checkNewDate():
    curr_date = (datetime.utcnow() + timedelta(hours=10)).date()
    with open('questions/todayQuestion.json', 'r') as readFile:
        today = json.load(readFile)
    return str(curr_date) != today["TODAYDATE"]


# The following code is used to retrieve and generate a new questions list. This should rarely be run

def sortQuestions(questions, easy, medium, hard):
    for i, q in enumerate(questions):
        i += 1
        if not q["paidOnly"]:
            difficulty = q["difficulty"]
            if difficulty == "Easy":
                easy.append(i)
            elif difficulty == "Medium":
                medium.append(i)
            else:
                hard.append(i)


def makeQuestionsList():
    questions = getAllQuestions()
    easy = []
    medium = []
    hard = []
    sortQuestions(questions, easy, medium, hard)
    questionsList = easy + medium
    random.shuffle(questionsList)
    questionsList = {"QUESTIONS": questionsList}
    with open('./questions/questionsList.json', 'w') as writeFile:
        json.dump(questionsList, writeFile)

# makeQuestionsList()           # only run this to regenerate the questions list. Try to avoid doing this!
