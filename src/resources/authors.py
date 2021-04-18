from datetime import datetime

from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from src import db
from src.database.models import Author
from src.schemas.authors import AuthorSchema


class AuthorListApi(Resource):
    author_schema = AuthorSchema()

    def get(self, uid=None):
        if not uid:
            authors = db.session.query(Author).all()
            return self.author_schema.dump(authors, many=True), 200
        author = db.session.query(Author).filter_by(id=uid).first()
        if not author:
            return '', 404
        return self.author_schema.dump(author), 200

    def post(self):
        try:
            author = self.author_schema.load(request.json, session=db.session)
        except ValidationError as e:
            return {'message': str(e)}, 400
        db.session.add(author)
        db.session.commit()
        return self.author_schema.dump(author), 201

    def put(self, uid):
        author = db.session.query(Author).filter_by(id=uid).first()
        if not author:
            return '', 404
        try:
            author = self.author_schema.load(request.json, instance=author, session=db.session)
        except ValidationError as e:
            return {'message': str(e)}, 400
        db.session.add(author)
        db.session.commit()
        return self.author_schema.dump(author), 200

    def patch(self, uid):
        author = db.session.query(Author).filter_by(id=uid).first()
        if not author:
            return '', 404
        author_json = request.json
        name = author_json.get('name')
        birthday = datetime.strptime(author_json.get('birthday'), '%B %d, %Y') if author_json.get(
            'birthday') else None
        is_active = author_json.get('is_active')

        if name:
            author.name = name
        elif birthday:
            author.birthday = birthday
        elif is_active:
            author.is_active = is_active

        db.session.add(author)
        db.session.commit()

        return {'message': 'Successfully updated'}, 200

    def delete(self, uid):
        author = db.session.query(Author).filter_by(id=uid).first()
        if not author:
            return '', 404
        db.session.delete(author)
        db.session.commit()
        return '', 204
