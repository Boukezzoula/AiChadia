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
from models import TranslateModel, UserModel
from schemas import TranslationSchema

blp = Blueprint("Translations", __name__, description="Operations on translations")


@blp.route("/translations/<string:translation_id>")
class Translations(MethodView):
    @jwt_required()
    @blp.response(200, TranslationSchema)
    def get(self, translation_id):
        translation = TranslateModel.query.get_or_404(translation_id)
        return translation

    @jwt_required()
    @blp.response(200, TranslationSchema)
    def delete(self, translation_id):
        translation = TranslateModel.query.get_or_404(translation_id)
        db.session.delete(translation)
        db.session.commit()
        return {"message": "Translation deleted."}, 200


@blp.route("/translations")
class TranslationsList(MethodView):
    @jwt_required()
    def get(self):
        translations = TranslateModel.query.all()
        all_translations = [{'id': translation.id, 'video_url': translation.video_url,
                      'video_script': translation.video_script, 'user_id': translation.user_id
                      } for translation in translations]
        return jsonify(all_translations), 200

    @jwt_required()
    @blp.arguments(TranslationSchema)
    def post(self, translation_data):
        #jwt = get_jwt()

        user_id = get_jwt_identity()
        #user_has_tokens = get_jwt_identity()
        print(user_id)
        #new_translation = TranslateModel(**translation_data)
        video_url = translation_data["video_url"]
        confirmIfExist = check_translation_in_db(video_url)
        print(confirmIfExist)
        if(confirmIfExist is not None):
            return confirmIfExist
            exit()


        # check if we already translated this video before
        #for translation in translations.values():
        #    if video_url == translation["video_url"]:
        #        return translation, 200
        #translation_id = uuid.uuid4().hex
        audio_local_path = get_video([video_url])
        script = generate_transcription(audio_local_path)
        #new_translation.video_script = script
        #new_translation.user_id = user_id
        #new_translation = {"id": translation_id, "video_url": video_url, "video_script": script}
        #translations[translation_id] = new_translation
        new_translation = TranslateModel(
            video_url=translation_data["video_url"],
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
    model = whisper.load_model("large")
    result = model.transcribe(audio_file_path, task='translate')
    # returns english translation text
    return result["text"]


def check_translation_in_db(url):
    translation = TranslateModel.query.filter(
        TranslateModel.video_url == url
    ).first()
    if(translation):
        return [{'script': translation.video_script}]
    else:
        return None

