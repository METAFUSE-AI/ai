from flask import Flask, request, jsonify
from flask_cors import CORS
import aichatbot
import aiGame
import emotion
import mysql.connector

app = Flask(__name__)
CORS(app)
# API 키는 환경 변수에서 자동으로 불러옵니다.
# .\.venv\Scripts\activate
# python app.py

print("app.py 파일 실행")

# aichatbot 모듈의 초기화 함수 호출
aichatbot.create_conversations_table()  # 데이터베이스 초기화

# 라우트 정의

@app.route('/')
def home():
    return "서버가 정상적으로 실행되었습니다!"

# AI Chatbot의 '/chat' 라우트
@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    return aichatbot.chat(data)

# AI Game의 '/game-result' 라우트
@app.route('/game-result', methods=['POST'])
def game_result():
    data = request.get_json()
    return aiGame.gameResult(data)

# Emotion Analysis의 '/encouragement' 라우트
@app.route('/encouragement', methods=['GET'])
def encouragement():
    return emotion.get_encouragement()

# 테스트 결과를 반환하는 라우트
@app.route('/test-result', methods=['GET'])
def test_result():
    user_id = request.args.get('userId')
    return aichatbot.test_result(user_id)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
