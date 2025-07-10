# utils/web_utils.py

import wikipedia

def search_wikipedia_summary(query):
    """
    Returns a short summary from Wikipedia for a given query.
    """
    try:
        wikipedia.set_lang("en")
        summary = wikipedia.summary(query, sentences=2)
        return summary
    except wikipedia.exceptions.DisambiguationError as e:
        return f"The topic '{query}' has multiple meanings. Try being more specific like: {e.options[0]}"
    except wikipedia.exceptions.PageError:
        return f"I couldn’t find a relevant Wikipedia page for '{query}'."
    except Exception as e:
        print("❌ Wikipedia Lookup Error:", e)
        return "An error occurred while trying to fetch the answer from Wikipedia."
