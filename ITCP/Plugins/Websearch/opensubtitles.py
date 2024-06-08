import os
import re
import sys
import json
import urllib
import urllib.request
import urllib.error

API_URL = 'https://api.opensubtitles.com/api/v1/'
API_URL_LOGIN = API_URL + 'login'
API_URL_LOGOUT = API_URL + 'logout'
API_URL_SEARCH = API_URL + 'subtitles'
API_URL_DOWNLOAD = API_URL + 'download'

APP_NAME = 'OpenSubtitlesDownload'
APP_VERSION = 'beta'
APP_API_KEY = 'qkTCqqBGqKUMo84WidqVfNOqosbkN3bJ'
USER_TOKEN = None

def getUserToken(username, password):
    headers = {
        "User-Agent": f"{APP_NAME} v{APP_VERSION}",
        "Api-key": f"{APP_API_KEY}",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    payload = {
        "username": username,
        "password": password
    }
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(API_URL_LOGIN, data=data, headers=headers)
    with urllib.request.urlopen(req) as response:
        response_data = json.loads(response.read().decode('utf-8'))
    return response_data['token']

def searchSubtitles(**kwargs):
    global USER_TOKEN
    try:USER_TOKEN = getUserToken('pamodmadubashana', 'pamod123')
    except Exception as e:
        print("Error while getting user token: " + str(e))
        return
    try:
        headers = {
            "User-Agent": f"{APP_NAME} v{APP_VERSION}",
            "Api-key": f"{APP_API_KEY}"
        }

        query_params = urllib.parse.urlencode(kwargs)
        url = f"{API_URL_SEARCH}?{query_params}"
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            response_data = json.loads(response.read().decode('utf-8')) 
        return response_data

    except (urllib.error.HTTPError, urllib.error.URLError) as err:
        print("Urllib error (", err.code, ") ", err.reason)
    except Exception:
        print("Unexpected error (line " + str(sys.exc_info()[-1].tb_lineno) + "): " + str(sys.exc_info()[0]))


def get_subtitle_by_file_id_from_opensubtitle(query , file_id):
    response_data = searchSubtitles(query=query, languages="en")
    if response_data:
        for data in response_data['data']:
            file_id = data['attributes']['files'][0]['file_id']
            if file_id == file_id:
                file_name = str(data['attributes']['files'][0]['file_name']).replace("\n","")
                subtitle_id = data['id']
                return file_name , subtitle_id

def get_result_from_opensubtitles(search_term,lang):
    response_data = searchSubtitles(query=search_term, languages=lang)
    results = []
    for data in response_data['data']:
        file_name = data['attributes']['files'][0]['file_name']
        file_id = data['attributes']['files'][0]['file_id']
        results.append(f"{file_name} b: {file_id}")
    return results



