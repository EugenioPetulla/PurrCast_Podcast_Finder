from cat.mad_hatter.decorators import tool
import requests


SPREAKER_API_BASE_URL = "https://api.spreaker.com/v2"


def get_author_info(author_id):
    endpoint = f"{SPREAKER_API_BASE_URL}/users/{author_id}"
    response = requests.get(endpoint)

    if response.status_code == 200:
        author_info = response.json()["response"]["user"]
        return author_info
    else:
        return None


@tool
def search_shows(query, cat):
    """
    Search for a podcast (a show). The input is a query.

    For example, search for a podcast about curious animals.
    Query -> curious animals
    """
    endpoint = f"{SPREAKER_API_BASE_URL}/search"
    settings = cat.mad_hatter.get_plugin().load_settings()

    params = {
        "type": "shows",
        "q": query,
        "limit": settings["number_of_results"],
    }
    response = requests.get(endpoint, params=params)

    if response.status_code == 200:
        results = response.json()["response"]["items"]
        shows_info = []
        for show in results:
            author_id = show["author_id"]
            author_info = get_author_info(author_id)
            author_name = author_info["fullname"] if author_info else "Unknown Author"
            shows_info.append(f"Show Name: {show['title']} by {author_name}\nLink: {show['site_url']}")
        return "\n".join(shows_info)
    else:
        return f"Error: {response.status_code}"


@tool
def search_episodes(query, cat):
    """
    Search for a podcast episode. The input is a query.

    For example, search for a podcast episode about Alice in wonderland.
    Query -> alice in wonderland
    """
    endpoint = f"{SPREAKER_API_BASE_URL}/search"
    settings = cat.mad_hatter.get_plugin().load_settings()
    
    params = {
        "type": "episodes",
        "q": query,
        "limit": settings["number_of_results"],
    }
    response = requests.get(endpoint, params=params)

    if response.status_code == 200:
        results = response.json()["response"]["items"]
        episodes_info = []
        for episode in results:
            show_title = episode["show"]["title"]
            episode_title = episode["title"]
            author_id = episode["show"]["author_id"]
            author_info = get_author_info(author_id)
            author_name = author_info["fullname"] if author_info else "Unknown Author"
            episodes_info.append(
                f"Show Title: {show_title}\nEpisode Title: {episode_title} by {author_name}\nLink: {episode['site_url']}")
        return "\n".join(episodes_info)
    else:
        return f"Error: {response.status_code}"
