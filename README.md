# youtube-video-chat-llm-app

This is a Shiny for Python app that fetches a Youtube video transcript and provides a LLM chat interface around it. It uses the [OpenAI API](https://github.com/openai/openai-python) for the LLM and [youtube-transcript-api](https://pypi.org/project/youtube-transcript-api/) package to get the Youtube video transcripts.

## Setup

The app expects that you have an OpenAI API key that you can paste into the input box. You can get one by visting the OpenAI API [quickstart page](https://platform.openai.com/docs/quickstart/).  

## Accessing the app

You can clone this repo and run the app locally or publish the app onto [Connect Cloud](https://connect.posit.cloud/). You may need to create a Connect Cloud account to access the app.

The app should work locally after you provide it your OpenAI API key. Note that publishing on a server like Connect Cloud will require you to [specify a https proxy for youtube-transcript-api](https://github.com/jdepoix/youtube-transcript-api) to be used during the requests to YouTube.