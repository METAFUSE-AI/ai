from flask import Flask, request, jsonify
from openai import OpenAI
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain.document_loaders import PyPDFLoader

from flask_cors import CORS  # CORS 모듈 가져오기


app = Flask(__name__)
CORS(app)  # 모든 도메인에서의 요청을 허용하도록 설정


client = OpenAI()

loader = DirectoryLoader('dataset', glob="*.pdf", loader_cls=PyPDFLoader)
documents = loader.load()

text_splitter=RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
chunks=text_splitter.split_documents(documents)

embedding = OpenAIEmbeddings()
vectordb=Chroma.from_documents(documents=chunks,embedding=embedding)
retriever=vectordb.as_retriever()

retriever=vectordb.as_retriever(search_kwargs={"k":2})

qa_chain=RetrievalQA.from_chain_type(
    llm=ChatOpenAI(model_name="gpt-4o-mini",temperature=0),
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=True
)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()

    # 사용자 입력 받기
    user_message = data.get('message', '')
    result=qa_chain.invoke(user_message)
    
    # response  = client.chat.completions.create(
    #     model="gpt-4o-mini",
    #     messages=[
    #         {"role": "system", "content": "You are a helpful assistant. You just answer me about metacognition.Please gently reject stories that are off-topic in metacognition"},
    #         {
    #             "role": "user",
    #             "content": user_message
    #         }
    #     ]
    # )

    # chatbot_reply = response.choices[0].message.content
    chatbot_reply=result['result']
    chatbot_reply += ' # sources :'
        
    for i, doc in enumerate(result['source_documents']):
        chatbot_reply +='['+str(i+1)+']'+doc.metadata['source']+' '
    print(chatbot_reply)
        
    return jsonify({'reply': chatbot_reply})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
