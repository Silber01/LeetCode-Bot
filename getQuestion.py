import discord
import requests

async def showQuestion(ctx, questionID):                        # calls method to get question with ID, and returns info
    embed = discord.Embed(title="LeetCode Bot")
    try:
        questionID = int(questionID)                            # safely cast questionID to an int
    except ValueError:                                          # if not an int, return an error message
        embed.colour = discord.Colour.red()
        embed.description = f"{questionID} is not a valid ID."
        await ctx.send(embed=embed)
        return
    question = await getQuestion(questionID)                    # call method to get question ID
    if question == "INVALID":                                   # if return is invalid, return an error message
        embed.colour = discord.Colour.red()
        embed.description = f"{questionID} is not a valid ID."
        await ctx.send(embed=embed)
        return
    question = dict(question)                                   # redundant, specifies that this is a dict to the code
    embed.colour = discord.Colour.purple()
    name = question["title"]
    difficulty = question["difficulty"]
    link = "https://leetcode.com/problems/" + question["titleSlug"] #titleSlug is what goes after /problems/ in the URL
    embed.description = f"\n**Name**: {name}\n**Difficulty**: {difficulty}\n\n {link}"
    await ctx.send(embed=embed)

def getQuestion(questionID):
    query = f"""query problemsetQuestionList($categorySlug: String, $limit: Int, $skip: Int, $filters: QuestionListFilterInput) {{
      problemsetQuestionList: questionList(
        categorySlug: $categorySlug
        limit: $limit
        skip: $skip
        filters: $filters
      ) {{
        total: totalNum
        questions: data {{
          difficulty
          title 
          titleSlug
          paidOnly: isPaidOnly
        }}
      }}
    }}"""
    params = f"""{{
      "categorySlug": "",
      "skip": {int(questionID)-1},
      "limit": 1,
      "filters": {{ 
      }}
    }}"""
    url = 'https://leetcode.com/graphql'                                # sends above query and params to this url
    r = requests.post(url, json={'query': query, 'variables': params})
    question = (r.json())["data"]["problemsetQuestionList"]["questions"]    # gets the problems returned from query
    try:
        question = question[0]                                          # may be empty if ID out of range
    except IndexError:
        return "INVALID"
    return question                                                     # return dict of question info
