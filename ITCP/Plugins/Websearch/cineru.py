import requests
from bs4 import BeautifulSoup


def get_response_from_cinerulk(search_query):
    search_query = str(search_query).replace(" ", "+")
    url = f"https://cineru.lk/?s={search_query}"
    response = requests.get(url)
    if response.status_code == 200:
        return BeautifulSoup(response.content, "html.parser")


def get_result_from_cineru(search_query):
    soup = get_response_from_cinerulk(search_query)
    results = soup.find_all("article", class_="item-list")
    web_results = []
    for result in results:
        title = str(result.find("h2", class_="post-box-title").text).replace("\n","")
        date = result.find("span", class_="tie-date").text
        web_results.append(f"{title}b:{date}")
    return web_results

def get_result_from_cineru_by_button_text(search_query,button_text):
    soup = get_response_from_cinerulk(search_query)
    results = soup.find_all("article", class_="item-list")
    web_results = []
    for result in results:
        title = str(result.find("h2", class_="post-box-title").text).replace("\n","").split("|")[0]
        if title == button_text:
            link = (result.find("h2", class_="post-box-title")).find("a")['href']
            return link
