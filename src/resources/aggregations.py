from flask_restful import Resource
from sqlalchemy import func

from src import db
from src.database.models import Book


class AggregationApi(Resource):
    def get(self):
        books_count = db.session.query(func.count(Book.id)).scalar()
        max_rating = db.session.query(func.max(Book.rating)).scalar()
        min_rating = db.session.query(func.min(Book.rating)).scalar()
        avg_rating = db.session.query(func.avg(Book.rating)).scalar()
        sum_rating = db.session.query(func.sum(Book.rating)).scalar()
        return {
            'count': books_count,
            'max': max_rating,
            'min': min_rating,
            'avg': avg_rating,
            'sum': sum_rating
        }
