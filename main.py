from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# URL của Rasa server
RASA_SERVER_URL = 'http://127.0.0.1:5005/webhooks/rest/webhook'

@app.route('/', methods=['POST', 'GET'])
def chat():
    if request.method == 'GET':
        return render_template('index_old.html')
    else:
        # Nhận tin nhắn từ form
        user_message = request.form['user_message']
        chat_content = request.form['chat_content']

        # Gửi tin nhắn đến Rasa
        response = send_message_to_rasa(user_message)

        # Xử lý phản hồi từ Rasa
        if response:
            bot_response = response[0]['text']
            chat_content += f"\n[BOT]: {bot_response}"

        return render_template('index_old.html', chat_content=chat_content)

def send_message_to_rasa(message):
    payload = {
        "sender": "test_user",  # Định danh người gửi tin nhắn
        "message": message  # Nội dung tin nhắn
    }
    try:
        r = requests.post(RASA_SERVER_URL, json=payload)
        r.raise_for_status()  # Nếu có lỗi, ném ra một ngoại lệ
        return r.json()
    except requests.exceptions.RequestException as e:
        print("Error sending message to Rasa:", e)
        return None

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
