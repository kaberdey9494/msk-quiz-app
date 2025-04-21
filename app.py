from flask import Flask, jsonify, send_from_directory
import random
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/")
def index():
    return send_from_directory("static", "index.html")

def get_question_from_radiopaedia(slug):
    url = f"https://radiopaedia.org/articles/{slug}"
    res = requests.get(url)
    if res.status_code != 200:
        return None

    soup = BeautifulSoup(res.content, "html.parser")
    content_div = soup.find("div", class_="article-section")
    if not content_div:
        return None

    text = content_div.get_text().replace("\n", " ").strip()
    sentences = text.split(". ")
    if len(sentences) < 5:
        return None

    question = sentences[0].strip() + "?"
    correct = sentences[1].strip()
    wrongs = [s.strip() for s in sentences[2:5]]

    options = [correct] + wrongs
    random.shuffle(options)

    return {
        "question": question,
        "options": options,
        "answer": correct
    }

@app.route("/generate")
def generate_dynamic():
    data = get_question_from_radiopaedia("hill-sachs-lesion")  # Geçici olarak sabit başlık
    if not data:
        return jsonify({"error": "No question found"})
    return jsonify(data)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
