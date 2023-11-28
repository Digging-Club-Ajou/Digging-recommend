from recommendSystem import UserRecommendationSystem
from flask import Flask, request, jsonify
from serverConnect import ServerManage
import json
import logging
import threading

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

recommend_system = UserRecommendationSystem(api_url="http://3.34.171.76:8080/api/ai")

server_config = ServerManage(app)
server_config.setup()

@app.route('/api/recommend/<int:user_id>', methods=['GET'])
def recommend(user_id):
    logger.info(f"Received recommendation request for user_id: {user_id}")
    try:
        with open("recommend.json", "r") as file:
            recommendation = json.load(file)
        if str(user_id) in recommendation:
            return jsonify(recommendation[str(user_id)])
        else:
            return jsonify({'error: user-id not founded in recommendations'}), 404
    
    except FileNotFoundError:
        logger.error("Recommendations file not found")
        return jsonify("not exisiting recommendations file"), 404
    except Exception as e:
        logger.error(f"An error occurred: {e}")

if __name__ == "__main__":
    scheduler_thread = threading.Thread(target=recommend_system.run_schedule)
    scheduler_thread.start()
    app.run(debug=True, port=5001) 