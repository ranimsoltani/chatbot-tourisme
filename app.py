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
    try:
        user_message = request.json.get("message")

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                     "role": "system",
                     "content": """
                    Tu es un assistant touristique expert.

                    Règles STRICTES :
                    - Tu réponds uniquement en français.
                    - Tu corriges automatiquement les fautes d’orthographe de l’utilisateur avant de répondre.
                    - Tu reformules correctement la phrase de l’utilisateur si elle contient des erreurs.
                    - Tu réponds uniquement sur le tourisme (voyages, hôtels, pays, villes, transport, culture, itinéraires).
                    - Si l'utilisateur pose une question hors sujet (informatique, médecine, maths, autre), tu refuses poliment.
                    - Tu réponds par : "Je suis spécialisé uniquement dans le tourisme."
                    - Tu restes toujours poli et utile.
                    """
                },
                {"role": "user", "content": user_message}
            ]
        )

        bot_reply = response.choices[0].message.content

        return jsonify({"reply": bot_reply})

    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == "__main__":
    app.run(debug=True)