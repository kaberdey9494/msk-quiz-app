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
    soup = BeautifulSoup(res.content, "html.parser")

    print("🧾 HTML:", soup.prettify()[:1000])

    content_div = (
        soup.find("div", class_="article-body") or
        soup.find("div", class_="article-section") or
        soup.find("article") or
        soup.find("div", id="main-content")
    )

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
    data = get_question_from_radiopaedia("hill-sachs-lesion")
    if not data:
        return jsonify({"error": "No question found"})
    return jsonify(data)

@app.route("/generate_test")
def generate_test():
    url = "https://radiopaedia.org/articles/hill-sachs-lesion"
    res = requests.get(url)
    soup = BeautifulSoup(res.content, "html.parser")
    print("🧾 TEST HTML:", soup.prettify()[:1000])
    return jsonify({"result": "HTML dumped to log"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
