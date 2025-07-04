import pyttsx3
from newsapi import NewsApiClient


# Initialize NewsAPI client
api_key = "e652956fe70548d2b5b85d07348800b4"  # Replace with your actual NewsAPI key
newsapi = NewsApiClient(api_key=api_key)

# Initialize text-to-speech engine
engine = pyttsx3.init()

def say(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()


def fetch_top_headlines():
    """Fetch top headlines and speak them out."""
    try:
        top_headlines = newsapi.get_top_headlines(
            language='en',
            country='us'
        )
        if top_headlines["articles"]:
            say("Here are the top headlines:")
            for i, article in enumerate(top_headlines["articles"][:5], start=1):  # Limit to 5 headlines
                say(f"Headline {i}: {article['title']}")
                print(f"Headline {i}: {article['title']}")
        else:
            say("No headlines available at the moment.")
            print("No headlines available.")
    except Exception as e:
        error_msg = f"An error occurred: {e}"
        say(error_msg)
        print(error_msg)

def fetch_all_articles(query):
    """Fetch articles related to a specific query and speak them out."""
    try:
        all_articles = newsapi.get_everything(
            q=query,
            language='en',
            sort_by='relevancy',
            page=1
        )
        if all_articles["articles"]:
            say(f"Here are the top articles about {query}:")
            for i, article in enumerate(all_articles["articles"][:5], start=1):  # Limit to 5 articles
                say(f"Article {i}: {article['title']}")
                print(f"Article {i}: {article['title']}")
        else:
            say(f"No articles found about {query}.")
            print(f"No articles found about {query}.")
    except Exception as e:
        error_msg = f"An error occurred: {e}"
        say(error_msg)
        print(error_msg)

def fetch_sources():
    """Fetch available news sources and speak them out."""
    try:
        sources = newsapi.get_sources(language='en')
        if sources["sources"]:
            say("Here are some available news sources:")
            for i, source in enumerate(sources["sources"][:10], start=1):  # Limit to 10 sources
                say(f"{i}. {source['name']} from {source['country']}")
                print(f"{i}. {source['name']} - {source['country']}")
        else:
            say("No sources available at the moment.")
            print("No sources available.")
    except Exception as e:
        error_msg = f"An error occurred: {e}"
        say(error_msg)
        print(error_msg)

if __name__ == "__main__":
    top_headlines = fetch_top_headlines()
    print(top_headlines)
