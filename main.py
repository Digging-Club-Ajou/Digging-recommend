from recommendSystem import UserRecommendationSystem
from flask import Flask, request, jsonify
from serverConnect import ServerManage

app = Flask(__name__)

server_config = ServerManage(app)
server_config.setup()

@app.route('api/ai-result/<int:memberId>', methods=['GET'])
def recommend():
    # server api link
    api_link = "http://3.34.171.76:8080/api/ai"
    user_idx = request.args.get('memberId', type=int)
    if user_idx is None:
        return jsonify({'error': 'User ID is required'}), 400
    
    user_recommend = UserRecommendationSystem(api_link)
    recommend_users = user_recommend.recommend_users(user_idx)
    
    return jsonify({
        'user_id': user_idx,
        'recommendations': recommend_users
    })

if __name__ == "__main__":
    app.run(debug=True)