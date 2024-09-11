from flask import Flask, request, jsonify
from openai import OpenAI

from flask_cors import CORS  # CORS 모듈 가져오기


app = Flask(__name__)
CORS(app)  # 모든 도메인에서의 요청을 허용하도록 설정


client = OpenAI()



@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()

    # 사용자 입력 받기
    user_message = data.get('message', '')
    
    response  = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant. You just answer me about metacognition.Please gently reject stories that are off-topic in metacognition"},
            {
                "role": "user",
                "content": user_message
            }
        ]
    )

    chatbot_reply = response.choices[0].message.content
    print(chatbot_reply)
        
    return jsonify({'reply': chatbot_reply})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
