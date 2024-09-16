from shiny import App, reactive, render, ui
from youtube_transcript_api import YouTubeTranscriptApi
from openai import AsyncOpenAI
import re
import os

try:
    from setup import api_key1
except ImportError:
    api_key1 = os.getenv("OPENAI_API_KEY")

app_info = """
This app provides a chat interface using the OpenAI API to answer questions about
a YouTube video based on its transcript.
"""

test_url1 = "https://www.youtube.com/watch?v=fKGoVefhtMQ&ab_channel=Dropout"
test_url2 = "https://youtu.be/fKGoVefhtMQ?feature=shared"

app_ui = ui.page_fillable(
    ui.h1("Youtube Video Transcript Chat"),
    ui.markdown(app_info),
    ui.row([
        ui.input_password(
            "api_key", 
            "OpenAI API Key",
            value = api_key1,
            width="25%"
        ),
        ui.input_text(
            "youtube_url", 
            "Enter YouTube URL:",
            placeholder="https://www.youtube.com/watch?v=...",
            value=test_url2,
            width="75%",
        )
        ]),
    ui.input_action_button("fetch_transcript", "Fetch Transcript"),
    ui.card(    
        ui.chat_ui("chat"),
        full_screen=True,
    ),
    fillable=True,
    fillable_mobile=True,
)

def server(input, output, session):
    Welcome=[
        {"role": "system", "content": """You are a helpful assistant
            that answers questions about a YouTube video based on its
            transcript."""},
        {"role": "assistant",
         "content": "**Hello!** How can I help you today?"},
    ]
    chat = ui.Chat(id="chat", messages=Welcome)
    # Fetch transcript from YouTube URL
    transcript = reactive.Value("")

    @reactive.Effect
    @reactive.event(input.fetch_transcript)
    async def fetch_transcript():
        url = input.youtube_url()
        if url:
            try:
                # if url is a shared link, extract the video id
                if "youtu.be" in url:
                    video_id = url.split("/")[-1].split("?")[0]
                # if url is a regular link, extract the video id
                else:
                    video_id = re.search(r"v=([^&]+)", url).group(1)
                transcript_data = YouTubeTranscriptApi.get_transcript(video_id)
                full_transcript = " ".join([entry['text'] for entry in transcript_data])
                transcript.set(full_transcript)
                await chat.append_message(
                    f"""Grabbing video transcript. 
                    Here's the video transcript: \n{transcript()}""")
                ui.notification_show("Transcript fetched successfully!", type="message")
            except Exception as e:
                ui.notification_show(f"Error fetching transcript: {e}", type="error")
                transcript.set("")
            
    @chat.on_user_submit  
    async def _():  
        if not transcript():
            ui.notification_show("Please fetch a transcript first.", type="warning")
            return
        api_key = input.api_key()
        if not api_key:
            ui.notification_show("Please enter your OpenAI API key.", type="error")
            return
        # Get messages currently in the chat
        messages = chat.messages(format="openai")
        # Create a response message stream
        api_key = input.api_key()
        llm = AsyncOpenAI(api_key=api_key)
        response = await llm.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            stream=True,
        )
        # Append the response stream into the chat
        await chat.append_message_stream(response)  


app = App(app_ui, server)
