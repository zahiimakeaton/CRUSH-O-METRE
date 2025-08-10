
import re
from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
import os

app = Flask(__name__)

# Your Gemini API key - set as environment variable or directly replace "YOUR_API_KEY_HERE"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "YOUR_API_KEY_HERE")
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")

# Assets mapping
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

Here are some examples:

Chat message: "I just can’t stop thinking about you, wanna hang out sometime?"  
Response: Rizz — Smooth moves! You're definitely making her smile 😎

Chat message: "Sorry, I’m really busy, maybe some other time."  
Response: Bro Zone — Friendly vibes only, no romance here 🤷‍♂️

Chat message: "I think we should just stay friends."  
Response: Cooked — Ouch, that’s a hard pass 🔥

Chat message: "I’m not sure, maybe we can see how things go?"  
Response: Maybe-Maybe — Playing it cool, keeping options open 🤔

Chat message: "Will you marry me?"  
Response: Marry Her — Straight to the point! True love alert 💍



Now analyze this chat message: "{user_text}"
"""

    try:
        response = model.generate_content(prompt)
        result_text = response.text.strip()

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

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)