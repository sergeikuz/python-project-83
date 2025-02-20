import os

import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import NamedTupleCursor

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')


class DatabaseConnection:
    def __enter__(self):
        self.connection = psycopg2.connect(DATABASE_URL)
        self.cursor = self.connection.cursor(cursor_factory=NamedTupleCursor)
        return self.cursor

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            print(f"Возникло исключение типа: {exc_type}, "
                  f"со значением: {exc_value}")
        self.cursor.close()
        self.connection.commit()
        self.connection.close()


class UrlRepository:
    def add_url(self, url):
        with DatabaseConnection() as cursor:
            cursor.execute(
                'INSERT INTO urls (name) VALUES (%s) RETURNING id',
                (str(url),)
            )
            result = cursor.fetchone()
            return result
    
    def get_all_urls(self):
        with DatabaseConnection() as cursor:
            query = (
                'SELECT \
                urls.id AS id, \
                urls.name AS name, \
                url_checks.created_at AS last_check, \
                status_code \
                FROM urls \
                LEFT JOIN url_checks \
                ON urls.id = url_checks.url_id \
                AND url_checks.id = ( \
                    SELECT max(id) FROM url_checks \
                    WHERE urls.id = url_checks.url_id \
                ) \
                ORDER BY urls.id DESC;'
            )
            cursor.execute(query)
            urls = cursor.fetchall()
            return urls

    def get_url_by_id(self, id):
        with DatabaseConnection() as cursor:
            cursor.execute(
                'SELECT * FROM urls WHERE id = (%s)',
                (id,)
            )
            result = cursor.fetchone()
            return result
        
    def get_url_by_name(self, name):
        with DatabaseConnection() as cursor:
            cursor.execute(
                'SELECT * FROM urls WHERE name = (%s)',
                (name,)
            )
            result = cursor.fetchone()
            return result
        
    def add_url_checks(self, data):
        with DatabaseConnection() as cursor:
            cursor.execute(
                'INSERT INTO url_checks \
                (url_id, status_code, h1, title, description) \
                VALUES \
                (%(url_id)s, %(status_code)s, %(h1)s, %(title)s, \
                %(description)s) \
                RETURNING id',
                data
            )

    def get_url_checks_by_id(self, id):
        with DatabaseConnection() as cursor:
            cursor.execute(
                'SELECT * FROM url_checks \
                WHERE url_id = (%s) ORDER BY id DESC',
                (id,)
            )
            result = cursor.fetchall()
            return result