from flask import Flask, request, jsonify
import openai 
from flask_cors import CORS  

app = Flask(__name__)
CORS(app)

# API 키는 환경 변수에서 자동으로 불러옵니다.

print("aiGame 실행 전")

@app.route('/game-result', methods=['POST'])
def gameResult():
    data = request.get_json()
    print("aiGame 실행")
    print(f"Received request method: {request.method}")
    print(f"Received game result: {data}")

    # 게임 결과 데이터를 받음
    game_stats = data.get('message', {})

    # 게임 결과 데이터를 텍스트로 변환하여 AI에 전달
    user_message = (f"나이: {game_stats['age']}세, 건강: {game_stats['health']}, 스트레스: {game_stats['stress']}, "
                    f"대인 관계: {game_stats['relationships']}, 돈: {game_stats['money']}. "
                    "이 사람은 끊임없는 선택의 연속 속에서 자신을 정의하고 있습니다. "
                    "이 선택들이 그의 삶에 어떤 영향을 미치고, 어떤 길을 만들어 나가는지에 대한 철학적 통찰을 제공해 주세요."
                    "응답은 1300자 이내로 하되, 문장이 자연스럽게 마무리되도록 하십시오."
                    "해당 game_stats를 바탕으로 해당 유저의 인생을 분석하여 응답을 5줄 이내로 작성해 주세요."
                    "이후 해당 game_stats에 대한 메타인지 피드백을 제공하며 삶에 대한 철학적인 통찰을 제공해 주세요.")

    # OpenAI에게 전달할 메시지 설정
    messages = [
        {
            "role": "system",
            "content": (
                "당신은 삶의 선택과 결과에 대해 문학적이고 철학적인 깊이 있는 통찰을 제공하는 전문가입니다. "
                "사용자가 마주한 인생의 선택과 그에 따른 결과를 탐구하는 방식으로 답변을 작성하세요. "
                "각 선택은 삶의 방향을 결정하는 중요한 순간이며, 사용자가 그 선택을 통해 어떤 존재로 "
                "형성될지에 대한 관점을 제공합니다."
            )
        },
        {"role": "user", "content": user_message}
    ]
    
    # AI 피드백 생성
    try:
        result = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages,
            temperature=0.8,
            max_tokens=500
        )
        chatbot_reply = result['choices'][0]['message']['content']
        print("AI 응답: ", chatbot_reply)  # AI 응답 출력
    except Exception as e:
        print(f"Error: {str(e)}")  # 발생한 오류 출력
        chatbot_reply = (
            "삶은 끊임없는 여정입니다. 당신이 맞닥뜨린 고난은 언젠가 빛나는 내일을 위한 밑거름이 될 것입니다. "
            "모든 것은 결국 지나가며, 당신은 더 강해질 것입니다."
        )
        
    print("AI 피드백 생성 완료")
    print(f"AI 피드백: {chatbot_reply}")
            
    return jsonify({'reply': chatbot_reply})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

