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

# 유저 추천클래스
class UserRecommendationSystem:
    def __init__(self, api_url):
        self.api_url = api_url
        self.logger = logging.getLogger(self.__class__.__name__)

    # spring 서버로부터 api fetch 하는 메소드
    def fetch_user_data(self):
        self.logger.info("Fetching user data")
        response = requests.get(self.api_url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception("Error fetching data from API")

    # 데이터 전처리 메소드
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
        df['age'] = (current_year - df['birthdate'].dt.year)

        # 나이 데이터에서 NaN 값을 기본 나이 값으로 대체
        default_age = 23
        df['age'].fillna(default_age, inplace=True)

        # 성별 데이터 인코딩 (null이 아닌 경우에만)
        mlb_gender = MultiLabelBinarizer()
        gender_encoded = mlb_gender.fit_transform(df['gender'].fillna('Unknown').astype(str))

        # 최종 특성 행렬 생성
        final_features = np.hstack([genre_encoded, artist_encoded, df[['age']], gender_encoded])
        return final_features
    
    # 유저 특성을 바탕으로 코사인 유사도 계산 메소드
    def calculate_cosine_similarity(self, user_features):
        return cosine_similarity(user_features)

    # json 업데이트 및 실행 메소드
    def calculate_and_save_recommendations(self, similarity_threshold=0.9, max_recommendations=5):
        self.logger.info("Calculating and saving recommendations")
        try:
            user_data = self.fetch_user_data()
            user_features = self.preprocess_user_data(user_data)
            similarity_matrix = self.calculate_cosine_similarity(user_features)
            
            recommendations = {}
            user_ids = [user['memberId'] for user in user_data['aiResponses']]  # 사용자 ID 목록 추출

            for user_idx, user_id in enumerate(user_ids):
                user_similarity = similarity_matrix[user_idx]
                
                # 유사도가 0.9 이상인 사용자들을 탐색
                similar_users = [(user_ids[idx], sim) for idx, sim in enumerate(user_similarity) if sim >= similarity_threshold and idx != user_idx]

                # 유사도가 높은 순서대로 정렬
                similar_users.sort(key=lambda x: x[1], reverse=True)

                # 유사도가 0.9 이상인 사용자가 3명 미만일 경우 상위 3명을 추천
                if len(similar_users) < 3:
                    similar_users = sorted(similar_users, key=lambda x: x[1], reverse=True)[:3]

                # 유사도가 0.9 이상인 사용자가 3명 이상일 경우 최대 5명 추천
                else:
                    similar_users = similar_users[:max_recommendations]

                similar_user_ids = [user_id for user_id, sim in similar_users]
                recommendations[str(user_id)] = similar_user_ids
            
            final_recommendations = {"memberIds": recommendations}

            with open("recommend.json", "w") as file:
                json.dump(final_recommendations, file)
            self.logger.info("Recommendations calculated and saved successfully")

        except Exception as e:
            self.logger.error(f"Error in calculate_and_save_recommendations: {e}")

# 스케쥴링 메소드
    def schedule_data(self):
        # 하루에 세 번 스케쥴링 되게끔 수정 (8시간 간격)
        schedule.every().day.at("02:00").do(self.calculate_and_save_recommendations)
        schedule.every().day.at("10:20").do(self.calculate_and_save_recommendations)
        schedule.every().day.at("18:00").do(self.calculate_and_save_recommendations)

# 스케쥴링 실행 메소드
    def run_schedule(self):
        self.schedule_data()
        while True:
            schedule.run_pending()
            time.sleep(60)
