import requests
import numpy as np
import pandas as pd
from datetime import datetime
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.metrics.pairwise import cosine_similarity
import json
import schedule
import time
import logging

class UserRecommendationSystem:
    def __init__(self, api_url):
        self.api_url = api_url
        self.logger = logging.getLogger(self.__class__.__name__)

    def fetch_user_data(self):
        self.logger.info("Fetching user data")
        response = requests.get(self.api_url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception("Error fetching data from API")

    # 데이터 전처리 함수
    def preprocess_user_data(self, user_data):
        # 중첩된 구조를 평탄화
        df = pd.json_normalize(user_data['aiResponses'])

        # MultiLabelBinarizer를 사용하여 리스트 데이터 인코딩
        mlb_genre = MultiLabelBinarizer()
        genre_encoded = mlb_genre.fit_transform(df['genres'])

        mlb_artist = MultiLabelBinarizer()
        artist_encoded = mlb_artist.fit_transform(df['artistNames'])

        # birthDate를 나이로 변환 (null이 아닌 경우에만)
        df['birthdate'] = pd.to_datetime(df['birthDate'], errors='coerce')
        current_year = datetime.now().year
        df['age'] = (current_year - df['birthdate'].dt.year).fillna(-1)

        # 성별 데이터 인코딩 (null이 아닌 경우에만)
        mlb_gender = MultiLabelBinarizer()
        gender_encoded = mlb_gender.fit_transform(df['gender'].fillna('Unknown').astype(str))

        # 나이를 정규화 또는 다른 방식으로 처리
        # 예: 나이가 null(-1)인 경우 평균 나이로 대체
        avg_age = df[df['age'] != -1]['age'].mean()
        df['age'] = df['age'].replace(-1, avg_age)
        
        # 최종 특성 행렬 생성
        final_features = np.hstack([genre_encoded, artist_encoded, df[['age']], gender_encoded])
        return final_features

    def calculate_cosine_similarity(self, user_features):
        return cosine_similarity(user_features)

    def calculate_and_save_recommendations(self):
        self.logger.info("Calculating and saving recommendations")
        user_data = self.fetch_user_data()
        user_features = self.preprocess_user_data(user_data)
        similarity_matrix = self.calculate_cosine_similarity(user_features)
        
        all_recommend = {}
        for user_idx in range(len(user_features)):
            user_similarity = similarity_matrix[user_idx]
            most_similar_users = np.argsort(user_similarity)[::-1][1:]
            all_recommend[user_idx] = most_similar_users[:3].tolist()
        
        with open("recommend.json", "w") as file:
            json.dump(all_recommend, file)           
        self.logger.info("Recommendations calculated and saved successfully")
    
    def schedule_data(self):
        schedule.every().day.at("00:01").do(self.calculate_and_save_recommendations)

    def run_schedule(self):
        
        self.schedule_data()
        while True:
            schedule.run_pending()
            time.sleep(60)
