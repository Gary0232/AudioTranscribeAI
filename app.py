from flask_sqlalchemy import SQLAlchemy
import os
import mimetypes
import hashlib
import ffmpeg
from flask import Flask, request, jsonify

from keyword_wiki_retrieval.dictionary_retrieval import get_local_definition
from keyword_wiki_retrieval.wiki_retrieval import get_wikipedia_info
from model import audio_recognition, qa, summarization
from flask_cors import CORS, cross_origin
from sqlalchemy import String, Column, Integer, Float, Text, ForeignKey, DateTime, JSON, ARRAY


app = Flask(__name__)

cors = CORS(app, resources=r'/*', supports_credentials=True)

FILE_UPLOAD_FOLDER = 'uploads'

ALLOWED_MIME_TYPES = ['audio/wav', 'audio/mpeg', 'audio/ogg', 'audio/x-flac', 'video/mp4']

base_bath = os.path.dirname(__file__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_bath, 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy()
db.init_app(app)


class ProcessedFile(db.Model):
    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(255), nullable=False)
    file_path = db.Column(Text, nullable=False)
    audio_recognition_result = db.Column(JSON)
    text_summarization_result = db.Column(Text)


# create the table if it doesn't exist
with app.app_context():
    db.create_all()

# create the folder if it doesn't exist
if not os.path.exists(FILE_UPLOAD_FOLDER):
    os.makedirs(FILE_UPLOAD_FOLDER)


@app.route("/file_upload", methods=['POST'])
@cross_origin()
def api_media_recognition():
    # Get the file from the request
    file = request.files.get('file')
    language = request.form.get('language')
    languages = {
        "en": "english",
        "ja": "japanese",
        "fr": "french",
        "de": "german",
        "es": "spanish",
        "ru": "russian"
    }

    if not file:
        return jsonify({"status": "error", "message": "No file provided"})
    if not language or language not in languages:
        return jsonify({"status": "error", "message": "Invalid language"})
    language_name = languages.get(language)

    # Check the file type using mimetypes
    mime_type, encoding = mimetypes.guess_type(file.filename)
    if mime_type not in ALLOWED_MIME_TYPES:
        return jsonify({"status": "error", "message": "Invalid file type"})

    # Generate a hash value as the filename
    hash_value = hashlib.md5(file.read()).hexdigest()
    file.seek(0)
    audio_filename = f"{hash_value}.mp3"
    audio_file = ProcessedFile.query.filter_by(name=audio_filename).first()
    if audio_file:
        # if the file has been processed before, return the result directly
        return jsonify({
            "status": "success",
            "hash": hash_value,
            "recognition_result": audio_file.audio_recognition_result
        })

    # else save the file and process it
    audio_filepath = os.path.join(FILE_UPLOAD_FOLDER, audio_filename)
    temp_file_path = os.path.join(FILE_UPLOAD_FOLDER, f"{hash_value}_temp")
    file.save(temp_file_path)

    # Extract audio with ffmpeg
    try:
        if mime_type == 'video/mp4':
            # Extract audio from video
            ffmpeg.input(temp_file_path).output(audio_filepath, codec='libmp3lame').run(overwrite_output=True)
        else:
            # Convert other audio formats to mp3
            ffmpeg.input(temp_file_path).output(audio_filepath, codec='libmp3lame').run(overwrite_output=True)
    except Exception as e:
        return jsonify({"status": "error", "message": f"Audio extraction failed: {e}"})
    finally:
        # Remove the temporary video file
        os.remove(temp_file_path)

    # Process the audio file
    result = audio_recognition(audio_filepath, language_name)
    print(result)

    # Store file info in the database
    processed_file = ProcessedFile(
        name=audio_filename,
        file_path=audio_filepath,
        audio_recognition_result=result
    )
    db.session.add(processed_file)
    db.session.commit()

    return jsonify({
        "status": "success",
        "hash": hash_value,
        "recognition_result": result
    })


@app.route("/wikipedia", methods=['GET'])
@cross_origin()
def api_wikipedia():
    keyword = request.args.get('keyword')
    if not keyword:
        return jsonify({"status": "error", "message": "No keyword provided"})
    title, url, summary, images_url = get_wikipedia_info(keyword)
    # get local dictionary meaning
    meaning = get_local_definition(keyword)
    return jsonify({
        "status": "success",
        "wikipedia_result": {
            "title": title,
            "url": url,
            "summary": summary,
            "images_url": images_url,
            "definition": meaning
        }
    })

@app.route("/summarize", methods=['POST'])
@cross_origin()
def api_text_summarization():
    # get the text from the request
    text = request.json.get('text')
    hash_value = request.json.get('hash')
    if not text:
        return jsonify({"status": "error", "message": "No text provided"})
    processed_file = ProcessedFile.query.filter_by(name=f"{hash_value}.mp3").first()
    if processed_file.text_summarization_result:
        return jsonify({
            "status": "success",
            "summarization_result": processed_file.text_summarization_result
        })
    # process the text
    summarized_text = summarization(text)
    return jsonify({
        "status": "success",
        "summarization_result": summarized_text
    })


@app.route("/qa", methods=['POST'])
@cross_origin()
def api_qa():
    question = request.json.get('question')
    file_hash = request.json.get('hash')
    if not question or not file_hash:
        return jsonify({"status": "error", "message": "No question or hash provided"})
    processed_file = ProcessedFile.query.filter_by(name=f"{file_hash}.mp3").first()
    if not processed_file:
        return jsonify({"status": "error", "message": "Invalid hash value"})
    # process the question
    answer = qa(processed_file.audio_recognition_result.get("text"), question)
    return jsonify({
        "status": "success",
        "answer": answer
    })


if __name__ == '__main__':
    app.run(debug=False, port=4000)
