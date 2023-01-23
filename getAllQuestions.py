import discord
import requests

def getAllQuestions():
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
      "skip": 0,
      "limit": 2543,
      "filters": {{ 
      }}
    }}"""
    url = 'https://leetcode.com/graphql'                                # sends above query and params to this url
    r = requests.post(url, json={'query': query, 'variables': params})
    questions_list = (r.json())["data"]["problemsetQuestionList"]['questions']   # gets the problems returned from query
    return questions_list      