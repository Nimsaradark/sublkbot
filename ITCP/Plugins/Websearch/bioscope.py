from bs4 import BeautifulSoup
import requests

def get_details_from_baiscope(search_term):
    search_term = str(search_term).replace(" ", "+")
    url = f"https://www.baiscope.lk/?s={search_term}"
    response = requests.get(url)
    if response.status_code == 200:
        return BeautifulSoup(response.content, "html.parser")
    else:
        return None

def get_result_for_search_term_from_baiscope(search_term):
    soup = get_details_from_baiscope(search_term)
    if soup:
        articles = soup.find_all("article")
        subtitles = []
        for article in articles:
            article_id = article.get('id')
            h2_tag = article.find("h2", class_="entry-title")
            if h2_tag:
                a_tag = h2_tag.find('a')
                if a_tag:
                    title = a_tag.text
                    title = (str(title).split("|")[0]).replace("\r\n\t\t\t\t","")
                    subtitles.append(f"{article_id}:{title}")
        return subtitles
    else:
      return None

def get_subtitle_from_baiscope_by_id(search_term,post_id):
    soup = get_details_from_baiscope(search_term)
    if soup:
        article = soup.find("article",id=post_id)
        h2_tag = article.find("h2", class_="entry-title")     
        if h2_tag:
            a_tag = h2_tag.find('a')
            if a_tag:
                link = a_tag['href']
                return get_download_url(link)
    else:
        return None

def get_download_url(subtitle_url):
    response = requests.get(subtitle_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        download_div = soup.find("div", style="background-color: #f8f8f8; color: #ff3300 !important; display: block; font-size: 20px; font-weight: bold; border-radius: 5px; margin: 2px auto; padding: 5px; width: 330px; min-height: 30px;")

        if download_div:
            a_tag = download_div.find('a')
            if a_tag and 'href' in a_tag.attrs:
                return a_tag['href']
    return None
