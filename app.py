import streamlit as st
from dotenv import load_dotenv
load_dotenv()
import google.generativeai as genai 
import os

from youtube_transcript_api import YouTubeTranscriptApi

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

prompt = "You are a youtube video summarizer.You are given a youtube video transcript and you need to summarize the entire video and provide the important summary in points within 200-250 words.Please Provide the summary of the text given here"
##getting the transcript data from yt videos

def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[1]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)

        transcript=""
        for i in transcript_text:
            transcript +=" "+i['text']
        return transcript

    except Exception as e:
        raise e
##getting the  summary based on prompt fro google gemini
def generate_gemini_content(transcript_text,prompt):
    model=genai.GenerativeModel("gemini-pro")
    response= model.generate_content(prompt+transcript_text)
    return response.text

##streamlit app
st.title("Youtube Video Transcript Summarizer")
youtube_video_url = st.text_input("Enter the youtube video url")

if youtube_video_url:
    video_id = youtube_video_url.split("=")[1]
    st.image(f"https://img.youtube.com/vi/{video_id}/0.jpg",use_column_width=True)

if st.button("Get Detailed Notes"):
    transcript_text=extract_transcript_details(youtube_video_url)

    if transcript_text:
        summary=generate_gemini_content(transcript_text,prompt)
        st.markdown("##Detailed Notes")
        st.write(summary)