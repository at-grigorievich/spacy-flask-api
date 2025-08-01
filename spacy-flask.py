# pip install spacy
# pip install flask
# python -m spacy download ru_core_news_md
# python -m spacy download en_core_web_md

# input: {"source": "Он сказал что, приедет... завтра? но так и не приехал"}\
# output: {
#"sentences": [
#        "Он сказал что, приедет... завтра?",
#        "но так и не приехал"
#    ]
#}

import spacy
from flask import Flask, request, jsonify

app = Flask(__name__)

nlp_models = {
    "ru": spacy.load("ru_core_news_sm"),
    "en": spacy.load("en_core_web_sm"),
}

@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({'status': 'pong'})

@app.route('/split', methods=['POST'])
def split():
    data = request.get_json(force=True)
    text = data.get('source', '').strip()
    lang = data.get('lang', 'en').lower()
    
    if not text:
        return jsonify({'error': 'No text provided'}), 400

    if lang not in nlp_models:
        return jsonify({'error': f"Unsupported language '{lang}'"}), 400

    nlp = nlp_models[lang]
    doc = nlp(text)
    
    sentences = [sent.text.strip() for sent in doc.sents]

    return jsonify({'sentences': sentences})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)