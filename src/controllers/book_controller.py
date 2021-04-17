from src.database.models import Book


class BookController:
    @staticmethod
    def fetch_all_book(session):
        return session.query(Book)

    @classmethod
    def fetch_book_by_uid(cls, session, uid):
        return cls.fetch_all_book(session).filter_by(uid=uid).first()
