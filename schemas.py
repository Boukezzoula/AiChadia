from marshmallow import Schema, fields


class PlainTranslationSchema(Schema):
    id = fields.Str(dump_only=True)
    video_url = fields.Str(required=True)
    video_script = fields.Str(dump_only=True)


class PlainTranscriptionSchema(Schema):
    id = fields.Str(dump_only=True)
    video_url = fields.Str(required=True)
    video_script = fields.Str(dump_only=True)


class PlainUserSchema(Schema):
    id = fields.Str(dump_only=True)
    username = fields.Str(required=True)
    firstname = fields.Str(required=True)
    lastname = fields.Str(required=True)
    email = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)


class UserRegistrationSchema(Schema):
    id = fields.Str(dump_only=True)
    username = fields.Str(required=True)
    firstname = fields.Str(required=True)
    lastname = fields.Str(required=True)
    email = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)


class UserLoginSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)


class TranslationSchema(PlainTranslationSchema):
    user_id = fields.Int(required=False, load_only=True)
    user = fields.Nested(PlainUserSchema(), dump_only=True)


class TranscriptionSchema(PlainTranscriptionSchema):
    user_id = fields.Int(required=False, load_only=True)
    user = fields.Nested(PlainUserSchema(), dump_only=True)


class UserSchema(PlainUserSchema):
    translations = fields.List(fields.Nested(PlainTranslationSchema()), dump_only=True)
