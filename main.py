import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import webbrowser
import requests
from newsapi import NewsApiClient

# Initialize recognizer and TTS engine
listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

# Initialize NewsAPI client with your API key
newsapi = NewsApiClient(api_key='c8b42dee8b674d1eb0169c67c298b500')


# Talk function to make the assistant speak
def talk(text):
    engine.say(text)
    engine.runAndWait()


# Function to take voice command
def take_command():
    command = ""  # Initialize command with an empty string
    try:
        with sr.Microphone() as source:
            print('Listening...')
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'alexa' in command:
                command = command.replace('alexa', '')
                print(command)
    except Exception as e:
        print(f"Error: {str(e)}")
    return command


# Fetch and speak top 5 news headlines specific to India
def get_news():
    try:
        top_headlines = newsapi.get_top_headlines(language='en', country='en', page_size=5)
        articles = top_headlines['articles']
        news_list = [article['title'] for article in articles]
        return news_list
    except Exception as e:
        print(f"Error fetching news: {str(e)}")
        return ["Unable to fetch news at the moment."]


# Main function to run the assistant
def run_alexa():
    command = take_command()
    print(command)

    if 'play' in command:
        song = command.replace('play', '')
        talk(f'Playing {song}')
        pywhatkit.playonyt(song)

    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        talk(f'Current time is {time}')

    elif 'who is' in command:
        person = command.replace('who is', '')
        info = wikipedia.summary(person, 1)
        print(info)
        talk(info)

    elif 'joke' in command:
        talk(pyjokes.get_joke())

    elif 'news' in command:
        talk('Fetching the latest news...')
        news = get_news()
        for headline in news:
            talk(headline)

    elif 'weather' in command:
        talk('Which city?')
        city = take_command()
        get_weather(city)

    elif 'search' in command:
        search_query = command.replace('search', '')
        talk(f'Searching for {search_query}')
        pywhatkit.search(search_query)

    elif 'open mail' in command:
        talk('Opening Gmail')
        webbrowser.open('https://mail.google.com/')

    elif 'remind me to' in command:
        task = command.replace('remind me to', '').strip()
        talk('For how long? Say it in minutes.')
        minutes = int(take_command())
        set_reminder(task, minutes * 60)

    else:
        talk('Please say the command again.')


# Run the assistant in a loop
while True:
    run_alexa()
