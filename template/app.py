from shiny import App, reactive, render, ui
from openai import AsyncOpenAI
import os

try:
    from setup import api_key1
except ImportError:
    api_key1 = os.getenv("OPENAI_API_KEY")

app_ui = ui.page_fillable(
    ui.h1("Chat with OpenAI GPT-4o-mini model"),
    ui.input_password(
            "api_key", 
            "OpenAI API Key",
            value = api_key1,
    ),
    ui.p("Ask me anything!"),
    ui.card(
        ui.chat_ui("chat", fill = False),
        full_screen=True,
    ),
    fillable=True,
    fillable_mobile=True,
)

def server(input, output, session):
    chat = ui.Chat(
        id="chat",
        messages=[
            {"content": "Hello! How can I help you today?", "role": "assistant"},
        ],
    )
    
    @chat.on_user_submit  
    async def _():  
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
