from flask import Flask, jsonify
import random

app = Flask(__name__)

QUESTIONS = [
    {
        "question": "What is the typical location of a Hill-Sachs lesion?",
        "options": [
            "Posterolateral humeral head",
            "Anterior glenoid rim",
            "Distal radius",
            "Greater trochanter"
        ],
        "answer": "Posterolateral humeral head"      
    },
    {
        "question": "Which tendon is most commonly involved in rotator cuff tears?",
        "options": [
            "Supraspinatus",
            "Infraspinatus",
            "Subscapularis",
            "Teres minor"
        ],
        "answer": "Supraspinatus"
    }
]

@app.route("/")
def home():
    return "MSK Quiz App is running!"

@app.route("/generate")
def generate_question():
    q = random.choice(QUESTIONS)
    return jsonify(q)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
