from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

client = OpenAI(
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1"
)

app = Flask(__name__, static_folder='static', template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message")

    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": "You are a tourism assistant."},
            {"role": "user", "content": user_message}
        ]
    )
    bot_reply = response.choices[0].message.content
    return jsonify({"reply": bot_reply})
@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json.get("message")

        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": "You are a tourism assistant."},
                {"role": "user", "content": user_message}
            ]
        )

        bot_reply = response.choices[0].message.content

        return jsonify({"reply": bot_reply})

    except Exception as e:
        return jsonify({"error": str(e)})
    
    if __name__ == "__main__":
        app.run(debug=True)