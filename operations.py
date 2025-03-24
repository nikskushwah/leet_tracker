import json
import pandas as pd
import time

df = pd.read_csv('output.csv')

def find_ques(number):
    x = df[df['frontendQuestionId'] == number]
    question_slug = x[["titleSlug"]].iloc[0][0]
    difficulty = x[["difficulty"]].iloc[0][0]
    topics = x[["topicNames"]].iloc[0][0]
    return [question_slug,difficulty,topics]
