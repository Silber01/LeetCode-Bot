import discord
import random
import asyncio
import os
import json
import requests
from os.path import exists
from discord.ext import commands, tasks
from getQuestion import *
from lcUtils import *
from checkTime import *

# questions = getAllQuestions()
# easy = []
# medium = []
# hard = []

# def sortQuestions():
#     for i, q in enumerate(questions):
#         if not q["paidOnly"]:
#             difficulty = q["difficulty"]
#             if difficulty == "Easy":
#                 easy.append(i)
#             elif difficulty == "Medium":
#                 medium.append(i)
#             else:
#                 hard.append(i)

# sortQuestions()
# questions_id = easy + medium

# def storeQuestionId(questions_id):
#     with open('./questions/questionsList.json', 'r') as readFile:
#         questions_list = json.load(readFile)

#     questions_list = questions_id

#     with open('./questions/questionsList.json', 'w') as writeFile:
#         json.dump(questions_list, writeFile)


# def shuffleID():
#     random.shuffle(questions_id)
#     storeQuestionId(questions_id)


# with open('./questions/questionsList.json', 'w') as writeFile:
#     json.dump(random.shuffle(questions_id), writeFile)

def getTodayQuestion():

    with open('./questions/todayQuestion.json', 'r') as readFile:
        today = json.load(readFile)

    with open('./questions/questionsList.json', 'r') as readFile:
        questions_list = json.load(readFile)

    today_id = today["LAST_INDEX"] + 1
    today_question = getQuestion(questions_list[today_id])

    today["LAST_INDEX"] += 1
    today["TODAY_DATE"] = datetime.now().date().isoformat()
    
    with open('todayQuestion.json', 'w') as writeFile:
        json.dump(today, writeFile)

    return today_question


def dailyQuestion():
    if checkNewDate() and check6AmPST():    
        question = getTodayQuestion()
        url = "https://leetcode.com/problems/" + question["titleSlug"]
        diff = question["difficulty"].lower()
        title = question["title"]
        output = f"Today's {diff} question: {title} \n {url} \n if you're new, do `-help` to learn how to play"

    print(output)
