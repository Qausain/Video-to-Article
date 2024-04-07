import streamlit as st
import openai
from youtube_transcript_api import YouTubeTranscriptApi
st.set_page_config(page_title="Youtube Video to Article", page_icon="📝")
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.markdown("""
    <style>
        .header {
            font-size: 46px;
            color: #FDFEFF; /* Change the color as per your preference */
            background-color: #f50000;
            text-align: center;
            margin-bottom: 30px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2); /* Add shadow effect */
        }
        .head {
            font-size: 16px;
            color: #FDFEFF; /* Change the color as per your preference */
            background-color: #f50000;
            text-align: left;
            margin-bottom: 30px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2); /* Add shadow effect */
        }
        .response {
            font-size: 34px;
            color: red; /* Change the color as per your preference */
            text-align: left;
            margin-bottom: 20px;
        }
        
    </style>
""", unsafe_allow_html=True)

created_style = """
    color: #888888; /* Light gray color */
    font-size: 99px; /* Increased font size */
""" 

@st.cache_data(show_spinner=False)
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



def extract_transcript(video_id):
    """Extracts the transcript from a YouTube video."""
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        for transcript in transcript_list:
            transcript_text_list = transcript.fetch()
            lang = transcript.language
            transcript_text = ""
            if transcript.language_code == 'en':
                for line in transcript_text_list:
                    transcript_text += " " + line["text"]
                return transcript_text
            elif transcript.is_translatable:
                english_transcript_list = transcript.translate('en').fetch()
                for line in english_transcript_list:
                    transcript_text += " " + line["text"]
                return transcript_text
        st.info("Transcript extraction failed. Please check the video URL.")
    except Exception as e:
        st.info(f"Error: {e}")

st.markdown("<p style='{}'>➡️created by 'Muhammad Zain Attiq'</p>".format(created_style), unsafe_allow_html=True)
st.markdown('<h1 class="header">Youtube Video to Article</h1>', unsafe_allow_html=True)
with st.expander("About the app..."):
    st.markdown('<h1 class="head">What the App Can Do: </h1>', unsafe_allow_html=True)
    st.write("The YouTube Video to Article app converts the videos into Engaging and interesting articles. It basically extracts transcripts from YouTube videos. It automatically detects the language and translates non-English transcripts to English. And then it convert these transcsripts into beautiful articles. Users can preview videos and access transcripts in real-time.")

    st.markdown('<h1 class="head">How to use this app: </h1>', unsafe_allow_html=True)
    st.markdown("""
    1. Input the YouTube video URL.
    2. Preview the video.
    3. Click "Generate Article" to extract the transcript and generate an article based on it.
    4. View and share the generated article.

    Developed by Muhammad Zain Attiq, the app offers a simple yet powerful tool for extracting video transcripts and converting them into well-structured articles.""")

video_url = st.text_input("Enter the video link: ")
if video_url:
    video_id = video_url.split("=")[1]
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)
submit = st.button("Generate Article")
    
if submit:
    transcript = ""
    with st.spinner("Generating Transcript..."):
        transcript = extract_transcript(video_id)
    if transcript:
        with st.spinner("Generating Article..."):
            article = generate_article(transcript)
            st.write("-----------------------------------------------------------------------------------")
            st.markdown('<h1 class="response">Here is the Article: </h1>', unsafe_allow_html=True)
            st.write(article)

