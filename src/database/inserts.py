from datetime import date

from src import db
from src.database.models import Author


def books():
    book1 = Author(
        name='Farrar, Straus and Giroux',
        birthday=date(1900, 1, 1)
    )
    book2 = Author(
        name='Wednesday Books',
        birthday=date(1900, 1, 1)
    )
    book3 = Author(
        name='Tor Books',
        birthday=date(1900, 1, 1)
    )
    book4 = Author(
        name='Forge Books',
        birthday=date(1900, 1, 1)
    )

    db.session.add(book1)
    db.session.add(book2)
    db.session.add(book3)
    db.session.add(book4)

    db.session.commit()
    db.session.close()


if __name__ == '__main__':
    print('Adding book in db...')
    books()
    print('Successfully adding!')
