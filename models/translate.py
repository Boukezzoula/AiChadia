from db import db


class TranslateModel(db.Model):
    __tablename__ = "translations"

    id = db.Column(db.Integer, primary_key=True)
    video_url = db.Column(db.String, unique=False, nullable=False)
    video_script = db.Column(db.Text, unique=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    #user = db.relationship("UserModel", back_populates="translations")
