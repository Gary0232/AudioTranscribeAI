from flask import Flask, request, jsonify

from keyword_wiki_retrieval.wiki_retrieval import get_wikipedia_info
from model import audio_recognition
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/file_upload", methods=['POST'])
def api_media_recognition():
    # get the file from the request
    file = request.files['file']
    if not file:
        return jsonify({"status": "error", "message": "No file provided"})
    # process the file
    result = audio_recognition(file.filename)
    return jsonify({
        "status": "success",
        "recognition_result": result
    })


@app.route("/wikipedia", methods=['GET'])
def api_wikipedia():
    keyword = request.args.get('keyword')
    print(keyword)
    if not keyword:
        return jsonify({"status": "error", "message": "No keyword provided"})
    # process the keyword
    # title, url, parsed = get_wikipedia_info(keyword)
    return jsonify({
        "status": "success",
        "wikipedia_result": keyword
    })

@app.route("/summarize", methods=['POST'])
def api_text_summarization():
    # get the text from the request
    text = request.json.get('text')
    if not text:
        return jsonify({"status": "error", "message": "No text provided"})
    # process the text
    # summarized_text = text_summarization(text)
    return jsonify({
        "status": "success",
        "summarization_result": text
    })



if __name__ == '__main__':
    app.run(debug=True)
