import requests
from bs4 import BeautifulSoup

def get_details_from_zoom(search_term):
    url = f'https://zoom.lk/?s={str(search_term).replace(" ", "+")}'
    response = requests.get(url)
    if response.status_code == 200:
        return BeautifulSoup(response.content, "html.parser")
    else:
        return None
    
def get_result_for_search_term_from_zoomlk(search_term):
    soup = get_details_from_zoom(search_term)
    if soup:
        articles = soup.find_all("div",class_="td_module_16 td_module_wrap td-animation-stack")
        subtitles = []
        for article in articles:
            link = article.find("a")["href"]
            title = article.find("a").get("title")
            date = article.find("span",class_="td-post-date").find("time")["datetime"]
            subtitles.append(f"{link}b:{title}b:{date}")
        return subtitles
    else:
      return None
        
def get_subtitle_from_zoomlk_by_date(search_term,date):
    soup = get_details_from_zoom(search_term)
    if soup:
        articles = soup.find_all("div",class_="td_module_16 td_module_wrap td-animation-stack")
        for article in articles:
            link = article.find("a")["href"]
            post_date = article.find("span",class_="td-post-date").find("time")["datetime"]
            if post_date == date:
                return link
    return None

def get_download_link_from_zoomlk(URL):
    response = requests.get(URL)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        link = soup.find("a", class_="download-button")["href"]
        return link 
    return None 
