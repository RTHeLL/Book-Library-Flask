"""
SELECT QUERIES
"""
from src import db
from src.database import models

books = db.session.query(models.Book).all()
