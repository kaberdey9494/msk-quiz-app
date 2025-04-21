from flask import Flask, jsonify, send_from_directory
import requests
from bs4 import BeautifulSoup
import random

app = Flask(__name__)

@app.route("/")
def index():
    return send_from_directory("static", "index.html")

def fetch_radiologyassistant_section(slug):
    url = "https://radiologyassistant.nl/musculoskeletal/bone-tumors/alphabetical-order/bone-tumor-p-z"
    res = requests.get(url)
    if res.status_code != 200:
        return None

    soup = BeautifulSoup(res.text, "html.parser")
    # Örnek olarak sadece 'Tug Lesion' başlığı altındaki içeriği alıyoruz:
    tug_section = soup.find(id=slug)
    if not tug_section:
        return None

    content = []
    for sib in tug_section.find_all_next():
        if sib.name == "h3":  # bir sonraki başlığa geldiyse dur
            break
        content.append(sib.get_text(strip=True))

    full_text = " ".join(content)
    sentences = full_text.split(". ")
    if len(sentences) < 4:
        return None

    question = f"What is true about Tug Lesion?"
    correct = sentences[0]
    wrongs = sentences[1:4]

    options = [correct] + wrongs
    random.shuffle(options)

    return {
        "question": question,
        "options": options,
        "answer": correct
    }

@app.route("/generate")
def generate():
    data = fetch_radiologyassistant_section("tug-lesion")
    if not data:
        return jsonify({"error": "No question found"})
    return jsonify(data)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)

