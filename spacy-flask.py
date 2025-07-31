# pip install spacy
# pip install flask
# python -m spacy download ru_core_news_md
# python -m spacy download en_core_web_md

# input: {"text": "Он сказал что, приедет... завтра? но так и не приехал"}\
# output: {
#"sentences": [
#        "Он сказал что, приедет... завтра?",
#        "но так и не приехал"
#    ]
#}

import spacy
from flask import Flask, request, jsonify

app = Flask(__name__)

nlp = spacy.load("en_core_web_md")

@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({'status': 'pong'})

@app.route('/split', methods=['POST'])
def split():
    data = request.get_json(force=True)
    text = data.get('source', '')
    if not text:
        return jsonify({'error': 'No text provided'}), 400

    doc = nlp(text)
    sentences = [sent.text.strip() for sent in doc.sents]

    return jsonify({'sentences': sentences})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)