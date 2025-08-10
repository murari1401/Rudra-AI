import wikipedia

def search_wikipedia(query):
    try:
        result = wikipedia.summary(query, sentences=2)
        return result
    except Exception as e:
        return "Sorry, I couldn't find anything."
