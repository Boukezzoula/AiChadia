from flask import jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
import whisper
import os
import yt_dlp
import tempfile
from sqlalchemy.exc import SQLAlchemyError
from db import db
from models import TranscribeModel
from schemas import TranscriptionSchema

blp = Blueprint("Transcriptions", __name__, description="Operations on Transcriptions")


@blp.route("/transcriptions/<string:transcription_id>")
class Translations(MethodView):
    @jwt_required()
    @blp.response(200, TranscriptionSchema)
    def get(self, transcription_id):
        transcription = TranscribeModel.query.get_or_404(transcription_id)
        return transcription

    @jwt_required()
    @blp.response(200, TranscriptionSchema)
    def delete(self, transcription_id):
        transcription = TranscribeModel.query.get_or_404(transcription_id)
        db.session.delete(transcription)
        db.session.commit()
        return {"message": "Transcriptions deleted."}, 200


@blp.route("/transcriptions")
class TranslationsList(MethodView):
    @jwt_required()
    def get(self):
        transcriptions = TranscribeModel.query.all()
        all_transcriptions = [{'id': transcription.id, 'video_url': transcription.video_url,
                               'video_script': transcription.video_script, 'user_id': transcription.user_id
                      } for transcription in transcriptions]
        return jsonify(all_transcriptions), 200

    @jwt_required()
    @blp.arguments(TranscriptionSchema)
    def post(self, transcription_data):
        user_id = get_jwt_identity()
        print(user_id)
        video_url = transcription_data["video_url"]
        audio_local_path = get_video([video_url])
        script = generate_transcription(audio_local_path)
        new_translation = TranscribeModel(
            video_url=transcription_data["video_url"],
            video_script=script,
            user_id=user_id
        )
        try:
            db.session.add(new_translation)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occured while creating the translation")

        translation = [{'script': new_translation.video_script}]
        return jsonify(translation), 201


def get_video(urls):
    temp_dir = tempfile.gettempdir()

    ydl = yt_dlp.YoutubeDL({
        'quiet': True,
        'verbose': False,
        'format': 'bestaudio',
        "outtmpl": os.path.join(temp_dir, "%(id)s.%(ext)s"),
        'postprocessors': [{'preferredcodec': 'mp3', 'preferredquality': '192', 'key': 'FFmpegExtractAudio', }],
    })

    paths = {}

    for url in urls:
        result = ydl.extract_info(url, download=True)
        print(
            f"Downloaded video \"{result['title']}\". Generating subtitles..."
        )
        paths["downloaded_audio"] = os.path.join(temp_dir, f"{result['id']}.mp3")
        local_path = paths["downloaded_audio"]
    return local_path


@jwt_required()
def generate_transcription(audio_file_path):
    # load the best model
    # change the model from large to medium
    model = whisper.load_model("large")
    result = model.transcribe(audio_file_path)
    # returns transcribed text
    return result["text"]