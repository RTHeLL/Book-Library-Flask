import datetime
import threading

import bs4 as bs4
import requests as requests
from flask_restful import Resource
from flask import request

from src import db
from src.controllers.book_controller import BookController
from concurrent.futures.thread import ThreadPoolExecutor as PoolExecutor


class PopulateDB(Resource):
    url = 'https://openlibrary.org'

    def post(self):
        threads = []
        books_to_create = []
        t0 = datetime.datetime.now()
        books_urls = self.get_books_urls(request.json['category'])
        for book_url in books_urls:
            threads.append(threading.Thread(target=self.parse_books, args=(book_url, books_to_create), daemon=True))
        [thread.start() for thread in threads]
        [thread.join() for thread in threads]
        created_books = self.populate_db_with_books(books_to_create)
        dt = datetime.datetime.now() - t0
        print(f'Add {created_books} new books in DB.\n'
              f'Completed for {dt.total_seconds():.2f} sec')
        return {'message': f'Add {created_books} new books in DB for {dt.total_seconds():.2f} sec'}, 201

    def get_books_urls(self, category):
        url = self.url + '/subjects/' + category
        resp = requests.get(url)
        resp.raise_for_status()

        html = resp.text
        bs = bs4.BeautifulSoup(html, features='html.parser')
        book_containers = bs.find_all('div', class_='book-cover')
        books_urls = [book.a.attrs['href'] for book in book_containers]
        return books_urls

    def parse_books(self, book_url, books_to_create):
        url = self.url + book_url
        book_content = requests.get(url)
        book_content.raise_for_status()

        html = book_content.text
        bs = bs4.BeautifulSoup(html, features='html.parser')
        title = bs.find('h1', class_='work-title').text
        try:
            rating = float(bs.find('span', itemprop='ratingValue').text)
        except AttributeError:
            rating = 0
        description = bs.find('div', class_='book-description').find('p').text.strip()
        distributed_by = bs.find('a', itemprop='author').text
        release_date = bs.find('div', class_='smallest gray sansserif').text.split('|')
        try:
            release_date = datetime.datetime.strptime(release_date[0].strip(), '%B %d, %Y').date()
        except ValueError:
            release_date = datetime.datetime.now().date()
        try:
            length = int(bs.find('span', class_='edition-pages').text)
        except AttributeError:
            length = 0
        books_to_create.append(
            {
                'title': title,
                'rating': rating,
                'description': description,
                'distributed_by': distributed_by,
                'release_date': release_date,
                'length': length
            }
        )
        return books_to_create

    @staticmethod
    def populate_db_with_books(books):
        return BookController.bulk_create_books(db.session, books)


class PopulateDBWithPoolExecutor(Resource):
    url = 'https://openlibrary.org'

    def post(self):
        t0 = datetime.datetime.now()
        books_urls = self.get_books_urls(request.json['category'])
        work = []
        with PoolExecutor() as executor:
            for book_url in books_urls:
                f = executor.submit(self.parse_books, book_url)
                work.append(f)
        books_to_create = [f.result() for f in work]
        created_books = self.populate_db_with_books(books_to_create)
        dt = datetime.datetime.now() - t0
        print(f'Add {created_books} new books in DB.\n'
              f'Completed for {dt.total_seconds():.2f} sec')
        return {'message': f'Add {created_books} new books in DB for {dt.total_seconds():.2f} sec'}, 201

    def get_books_urls(self, category):
        url = self.url + '/subjects/' + category
        resp = requests.get(url)
        resp.raise_for_status()

        html = resp.text
        bs = bs4.BeautifulSoup(html, features='html.parser')
        book_containers = bs.find_all('div', class_='book-cover')
        books_urls = [book.a.attrs['href'] for book in book_containers]
        return books_urls

    def parse_books(self, book_url):
        url = self.url + book_url
        book_content = requests.get(url)
        book_content.raise_for_status()

        html = book_content.text
        bs = bs4.BeautifulSoup(html, features='html.parser')
        title = bs.find('h1', class_='work-title').text
        try:
            rating = float(bs.find('span', itemprop='ratingValue').text)
        except AttributeError:
            rating = 0
        description = bs.find('div', class_='book-description').find('p').text.strip()
        distributed_by = bs.find('a', itemprop='author').text
        release_date = bs.find('div', class_='smallest gray sansserif').text.split('|')
        try:
            release_date = datetime.datetime.strptime(release_date[0].strip(), '%B %d, %Y').date()
        except ValueError:
            release_date = datetime.datetime.now().date()
        try:
            length = int(bs.find('span', class_='edition-pages').text)
        except AttributeError:
            length = 0
        return {
            'title': title,
            'rating': rating,
            'description': description,
            'distributed_by': distributed_by,
            'release_date': release_date,
            'length': length
        }

    @staticmethod
    def populate_db_with_books(books):
        return BookController.bulk_create_books(db.session, books)


class PopulateDBWithOutThreading(Resource):
    url = 'https://openlibrary.org'

    def post(self):
        t0 = datetime.datetime.now()
        book_urls = self.get_books_urls(request.json['category'])
        books = self.parse_books(book_urls)
        created_books = self.populate_db_with_books(books)
        dt = datetime.datetime.now() - t0
        print(f'Add {created_books} new books in DB.\n'
              f'Completed for {dt.total_seconds():.2f} sec')
        return {'message': f'Add {created_books} new books in DB for {dt.total_seconds():.2f} sec'}, 201

    def get_books_urls(self, category):
        url = self.url + '/subjects/' + category
        resp = requests.get(url)
        resp.raise_for_status()

        html = resp.text
        bs = bs4.BeautifulSoup(html, features='html.parser')
        book_containers = bs.find_all('div', class_='book-cover')
        book_links = [book.a.attrs['href'] for book in book_containers][:10]
        return book_links

    def parse_books(self, book_urls):
        books_to_create = []
        for url in book_urls:
            url = self.url + url
            book_content = requests.get(url)
            book_content.raise_for_status()

            html = book_content.text
            bs = bs4.BeautifulSoup(html, features='html.parser')
            title = bs.find('h1', class_='work-title').text
            try:
                rating = float(bs.find('span', itemprop='ratingValue').text)
            except AttributeError:
                rating = 0
            description = bs.find('div', class_='book-description').find('p').text.strip()
            distributed_by = bs.find('a', itemprop='author').text
            release_date = bs.find('div', class_='smallest gray sansserif').text.split('|')
            try:
                release_date = datetime.datetime.strptime(release_date[0].strip(), '%B %d, %Y').date()
            except ValueError:
                release_date = datetime.datetime.now().date()
            try:
                length = int(bs.find('span', class_='edition-pages').text)
            except AttributeError:
                length = 0
            books_to_create.append(
                {
                    'title': title,
                    'rating': rating,
                    'description': description,
                    'distributed_by': distributed_by,
                    'release_date': release_date,
                    'length': length
                }
            )
        return books_to_create

    @staticmethod
    def populate_db_with_books(books):
        return BookController.bulk_create_books(db.session, books)
