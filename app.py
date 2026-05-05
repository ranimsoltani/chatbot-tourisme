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

                    Tu réponds uniquement sur :
                    - Voyages
                    - Tourisme
                    - Hôtels
                    - Pays et villes
                    - Transport (avion, train, etc.)
                    - Itinéraires de voyage
                    - Culture et attractions touristiques


                Tu réponds uniquement en français.


                Si l'utilisateur pose une question hors tourisme (programmation, médecine, maths, etc.):
                - Tu refuses poliment
                - Tu réponds exactement :
                "Je suis spécialisé uniquement dans le tourisme."


                - Clair et simple
                - Utile pour un voyageur
                - Structuré si possible (listes, conseils)

                Si l'utilisateur écrit avec des fautes :
                - Tu corriges la phrase
                - Tu commences ta réponse par :
                "Tu veux dire : <phrase corrigée>"
                - Ensuite tu continues avec la réponse touristique basée sur la phrase corrigée


                Ne jamais sortir du domaine du tourisme.
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