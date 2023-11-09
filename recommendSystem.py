import requests
import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics.pairwise import cosine_similarity

# user 추천 시스템 클래스
class UserRecommendationSystem:
    # 서버로부터 api
    def __init__(self, api_url):
        self.api_url = api_url

    def fetch_user_data(self):
        response = requests.get(self.api_url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception("Error")
    
    # 데이터 전처리 메소드
    def preprocess_user_data(self, user_data):
        df = pd.DataFrame(user_data)
        ohe = OneHotEncoder()
        genre_encoded = ohe.fit_transform(df[['genre']]).toarray()
        artist_encoded = ohe.fit_transform(df[['artist']]).toarray()
        gender_encoded = ohe.fit_transform(df[['gender']]).toarray()

        final_features = np.hstack([genre_encoded, artist_encoded, df[['age']].values, gender_encoded])
        return final_features

    # 코사인 유사도 메소드
    def calculate_cosine_similarity(self, user_features):
        return cosine_similarity(user_features)

    # 유저 추천 메소드
    def recommend_users(self, similarity_matrix, user_index):
        user_similarity = similarity_matrix[user_index]
        most_similar_user_index = np.argmax(user_similarity[1:]) + 1
        return most_similar_user_index
