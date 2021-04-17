from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from src.database.models import Author


class AuthorSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Author
        load_instance = True
