import time
import pandas as pd
from bs4 import BeautifulSoup
import requests
import json
import googletrans
from selenium.webdriver.common.by import By
from selenium import webdriver
from flask import Flask, request, jsonify

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

def get_nation(nation):
    return 'KO' if nation == '대한민국' else 'EN'

def get_gender_group(group):
    result = group.split(', ')
    gender = 'f' if result[0] == '여성' else 'm' if result[0] == '남성' else 'b'
    group_type = 'y' if result[1] == '그룹' else 'n'
    return gender, group_type

def translate(en_name_list):
    ko_name_list = []
    translator = googletrans.Translator()
    for item in en_name_list:
        translated = translator.translate(item, dest='ko')
        ko_name_list.append(translated.text)
    return ko_name_list

def crawler(artist_list):
    failed_artists = []
    driver = webdriver.Chrome(options=options)

    crawler_info = []
    for artist in artist_list:
        if artist in failed_artists:
            continue
        try:
            url = f'https://www.melon.com/search/total/index.htm?q={artist}&section=&searchGnbYn=Y&kkoSpl=Y&kkoDpType=&mwkLogType=T'
            driver.get(url)
            time.sleep(2)
            name = driver.find_element(By.XPATH, '//*[@id="conts"]/div[3]/div/div[1]/div/a/strong').text
            element = driver.find_element(By.XPATH, '//*[@id="conts"]/div[3]/div/div[1]/dl')
            lines = element.text.split('\n')
            genre = lines[7]
            crawler_info.append({'name': name, 'genre': genre})
        except:
            print(f"Failed to crawl artist: {artist}")
            failed_artists.append(artist)

    return crawler_info

genre_mapping = {
    'ballade': ['발라드'],
    'dance': ['댄스'],
    'rockMetal': ['록', '메탈'],
    'rbAndSoul': ['R&B', 'Soul'],
    'rapHiphop': ['랩', '힙합'],
    'folkBlues': ['포크', '블루스'],
    'indie': ['인디음악'],
    'pop': ['POP', 'J-POP', '라틴', '월드뮤직'],
    'ostAndMusical': ['국내드라마', '국내영화', '국외영화', '애니메이션', '웹툰', 'OST', '뮤지컬']
}

def convert(artist_info):
    final_info = []
    for item in artist_info:
        name = item['name']
        genres = item['genre'].split(', ')
        result_dict = {'artistName': name}
        for genre in genre_mapping:
            result_dict[genre] = 1 if any(g in genres for g in genre_mapping[genre]) else 0
        final_info.append(result_dict)
    return final_info

app = Flask(__name__)

def get_artist_info(artist_name):
    translated_name = translate([artist_name])[0]
    artist_info = []

    # 번역된 이름으로 먼저 크롤링 시도
    try:
        artist_info = crawler([translated_name])
        if not artist_info:  # 크롤링 결과가 없으면 원본 이름으로 재시도
            raise Exception("No results with translated name")
    except:
        print(f"Trying with original name for artist: {artist_name}")
        artist_info = crawler([artist_name])

    return convert(artist_info)

@app.route('/api/genres', methods=['POST'])
def get_genres():
    artist_responses = request.json.get('artistInfoRequests', [])
    results = []
    for artist_response in artist_responses:
        artist_name = artist_response.get('artistName', '')
        artist_info = get_artist_info(artist_name)
        results.extend(artist_info)
    return jsonify({'artistInfoResponses': results})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=7000)
