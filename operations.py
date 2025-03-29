import streamlit as st
import pandas as pd
import boto3
from io import StringIO

@st.cache_data(ttl=3600)
def load_csv_from_s3():
    s3 = boto3.client(
        "s3",
        aws_access_key_id=st.secrets["aws"]["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=st.secrets["aws"]["AWS_SECRET_ACCESS_KEY"]
    )

    bucket_name = st.secrets["aws"]["BUCKET_NAME"]
    file_key = st.secrets["aws"]["FILE_KEY"]

    csv_obj = s3.get_object(Bucket=bucket_name, Key=file_key)
    csv_string = csv_obj["Body"].read().decode('utf-8')
    
    return pd.read_csv(StringIO(csv_string))

df = load_csv_from_s3()

def find_ques(number):
    x = df[df['frontendQuestionId'] == number]
    question_slug = x[["titleSlug"]].iloc[0][0]
    difficulty = x[["difficulty"]].iloc[0][0]
    topics = x[["topicNames"]].iloc[0][0]
    return [question_slug, difficulty, topics]
