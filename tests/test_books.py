import http
import json
from dataclasses import dataclass
from unittest.mock import patch

import src.controllers.book_controller
from src import app


@dataclass
class TempBook:
    title = 'TempBook'
    distributed_by = 'Temp'
    release_date = '2018-4-18'
    description = 'Temp desc'
    length = 123
    rating = 4.2


class TestBooks:
    uid = []

    def test_get_books_with_db(self):
        client = app.test_client()
        resp = client.get('/books')

        assert resp.status_code == http.HTTPStatus.OK

    @patch('src.controllers.book_controller.BookController.fetch_all_book', autospec=True)
    def test_get_books_mock_db(self, mock_db_call):
        client = app.test_client()
        resp = client.get('/books')
        mock_db_call.assert_called_once()
        assert resp.status_code == http.HTTPStatus.OK
        assert len(resp.json) == 0

    def test_create_film_with_db(self):
        client = app.test_client()
        data = {
            'title': 'PyTest Title',
            'release_date': '1900-1-1',
            'distributed_by': '1',
            'description': '',
            'length': 100,
            'rating': 9.2
        }
        resp = client.post('/books', data=json.dumps(data), content_type='application/json')
        assert resp.status_code == http.HTTPStatus.CREATED
        assert resp.json['title'] == 'PyTest Title'
        self.uid.append(resp.json['uid'])

    def test_create_film_with_mock_db(self):
        with patch('src.db.session.add', autospec=True) as mock_session_add, \
                patch('src.db.session.commit', autospec=True) as mock_session_commit:
            client = app.test_client()
            data = {
                'title': 'PyTest Title',
                'release_date': '1900-1-1',
                'distributed_by': '1',
                'description': '',
                'length': 100,
                'rating': 9.2
            }
            resp = client.post('/books', data=json.dumps(data), content_type='application/json')
            mock_session_add.assert_called_once()
            mock_session_commit.assert_called_once()

    def test_update_film_with_db(self):
        client = app.test_client()
        data = {
            'title': 'PyTest Update',
            'distributed_by': 'PyTest Update dist',
            'release_date': '2021-4-18'
        }
        url = f'/books/{self.uid[0]}'
        resp = client.put(url, data=json.dumps(data), content_type='application/json')
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json['title'] == 'PyTest Update'

    def test_update_film_with_mock_db(self):
        with patch('src.controllers.book_controller.BookController.fetch_book_by_uid') as mocked_query, \
            patch('src.db.session.add', autospec=True) as mock_session_add, \
                patch('src.db.session.commit', autospec=True) as mock_session_commit:
            mocked_query.return_value = TempBook()
            client = app.test_client()
            data = {
                'title': 'PyTest Update',
                'distributed_by': 'PyTest Update dist',
                'release_date': '2021-4-18'
            }
            url = f'/books/{self.uid[0]}'
            resp = client.put(url, data=json.dumps(data), content_type='application/json')
            mock_session_add.assert_called_once()
            mock_session_commit.assert_called_once()

    def test_delete_with_db(self):
        client = app.test_client()
        url = f'/books/{self.uid[0]}'
        resp = client.delete(url)
        assert resp.status_code == http.HTTPStatus.NO_CONTENT
