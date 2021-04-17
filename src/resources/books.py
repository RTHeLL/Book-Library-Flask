from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from src import db
from src.controllers.book_controller import BookController
from src.database.models import Book
from src.resources.auth import token_required
from src.schemas.books import BookSchema


class BookListApi(Resource):
    book_schema = BookSchema()

    # @token_required
    def get(self, uid=None):
        if not uid:
            books = BookController.fetch_all_book(db.session).all()
            return self.book_schema.dump(books, many=True), 200
        book = BookController.fetch_book_by_uid(db.session, uid)
        if not book:
            return '', 404
        return self.book_schema.dump(book), 200

    def post(self):
        try:
            book = self.book_schema.load(request.json, session=db.session)
        except ValidationError as e:
            return {'message': str(e)}, 400
        db.session.add(book)
        db.session.commit()
        return self.book_schema.dump(book), 201

    def put(self, uid):
        book = BookController.fetch_book_by_uid(db.session, uid)
        if not book:
            return '', 404
        try:
            book = self.book_schema.load(request.json, instance=book, session=db.session)
        except ValidationError as e:
            return {'message': str(e)}, 400
        db.session.add(book)
        db.session.commit()
        return self.book_schema.dump(book), 200

    def patch(self, uid):
        book = BookController.fetch_book_by_uid(db.session, uid)
        if not book:
            return '', 404
        try:
            book = self.book_schema.load(request.get_json(), instance=book, partial=True, session=db.session)
        except ValidationError as e:
            return {'message': str(e)}, 400
        db.session.add(book)
        db.session.commit()
        return self.book_schema.dump(book), 200

    def delete(self, uid):
        book = BookController.fetch_book_by_uid(db.session, uid)
        if not book:
            return '', 404
        db.session.delete(book)
        db.session.commit()
        return '', 204
