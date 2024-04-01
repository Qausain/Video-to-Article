import streamlit as st
import pathlib
import openai
from youtube_transcript_api import YouTubeTranscriptApi

openai.api_key = st.secrets["OPENAI_API_KEY"]


def generate_article(transcript):
    system_prompt = """
    You are a youtube video to article converter. You will be taking the transcript text and converting it into a well organized article. You will be arranging the content of the transcript, putting headings, subheading and bullets & numberings where it required. In short you have to convert that video transcript into a beautiful, well-structured and Engaging article. The article should have a beautiful title. The titile should be the main heading and the content should be well formatted into subheading, bullets, numbering and paragraphs where they are required.
"""
    user_prompt = f"""
    Here is the transcript of the video: {transcript}
"""
    
    messages = [
        {'role': 'user', 'content': user_prompt},
        {'role': 'system', 'content':system_prompt}
    ]
    client = openai.OpenAI()
    response = client.chat.completions.create(
            model ="gpt-3.5-turbo",
            messages=messages,
            temperature=1.2,
            max_tokens=1000,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
    return response.choices[0].message.content



def extract_transcript(video_url):
    try:
        video_id = video_url.split("=")[1]
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages = ['en', 'ur', 'hi'])
        transcript_text = ""
        for i in transcript:
            transcript_text += " " + i["text"]
        
        return transcript_text
    except Exception as e:
        raise e


st.title("Youtube Video to Article")
video_url = st.text_input("Enter the video link: ")
video_id = video_url.split("=")[1]
if video_url:
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)
submit = st.button("Generate Article")
    
if submit:
    transcript = extract_transcript(video_url)
    # st.write(transcript)s
    if transcript:
        article = generate_article(transcript)
        st.write("-----------------------------------------------------------------------------------")
        st.write(article)
