from recommendSystem import UserRecommendationSystem


if __name__ == "__main__":
    # server api link
    api_link = "http://3.34.171.76:8080/api/ai"

    user_idx = 1
    user_recommend = UserRecommendationSystem(api_link)
    recommend_users = user_recommend.recommend_users(user_idx)

    print(f"User {user_idx}에게 추천되는 사용자들: {recommend_users}")