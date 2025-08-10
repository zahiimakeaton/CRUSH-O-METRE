import re
import os
from flask import Flask, request, jsonify, render_template
import google.generativeai as genai

app = Flask(__name__)

# Gemini API key from environment variable
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "YOUR_API_KEY_HERE")
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")

ASSETS = {
    "Rizz": {
        "image": "/static/images/rizz.gif",
        "audio": "/static/audio/rizz.mp3"
    },
    "Cooked": {
        "image": "/static/images/cooked.gif",
        "audio": "/static/audio/cooked.mp3"
    },
    "Bro Zone": {
        "image": "/static/images/brozone.gif",
        "audio": "/static/audio/brozone.mp3"
    },
    "Maybe-Maybe": {
        "image": "/static/images/maybe.gif",
        "audio": "/static/audio/maybe.mp3"
    },
    "Marry Her": {
        "image": "/static/images/marryher.gif",
        "audio": "/static/audio/marryher.mp3"
    }
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    user_text = data.get('text', '').strip()

    if not user_text:
        return jsonify({"error": "Please enter some chat text!"}), 400

    prompt = f"""
You are a witty and fun crush-o-meter AI. Analyze the chat message below and respond with:

1. Exactly one crush status label from: Rizz, Cooked, Bro Zone, Maybe-Maybe, Marry Her, Leave It.  
2. A short, playful explanation why you chose that label.  
3. A fitting emoji to match the mood.
4. Analyse the emoji given by the user also to make more sense

Format your answer like this (without quotes):  
"<Label> — <Explanation> <Emoji>"

Now analyze this chat message: "{user_text}"
"""

    try:
        response = model.generate_content(prompt)
        result_text = response.text.strip()

    except Exception as e:
        error_msg = str(e).lower()

       
        if "quota" in error_msg or "limit" in error_msg:
            return jsonify({
                "error": "The AI's daily charm quota is out 💔. Please try again tomorrow!"
            }), 429
        
        # Any other unexpected error
        return jsonify({
            "error": f"Unexpected server error: {str(e)}"
        }), 500

    # Parse the label from Gemini's response
    label_match = re.match(r"([\w\- ]+)\s*—", result_text)
    label = label_match.group(1).strip() if label_match else None

    if label not in ASSETS:
        label = "Maybe-Maybe"

    explanation = result_text.split('—', 1)[1].strip() if '—' in result_text else ""
    asset = ASSETS[label]

    return jsonify({
        "label": label,
        "explanation": explanation,
        "image": asset["image"],
        "audio": asset["audio"]
    })


def handler(request, *args, **kwargs):
    return app(request, *args, **kwargs)
