import psycopg2
from psycopg2.extras import NamedTupleCursor


class UrlRepository:
    def __init__(self, db_url):
        self.conn = psycopg2.connect(db_url)

    def add_url(self, url):
        with self.conn.cursor(cursor_factory=NamedTupleCursor) as cursor:
            cursor.execute(
                'INSERT INTO urls (name) VALUES (%s) RETURNING id',
                (str(url),)
            )
            result = cursor.fetchone()
            self.conn.commit()
            return result
    
    def get_all_urls(self):
        with self.conn.cursor(cursor_factory=NamedTupleCursor) as cursor:
            query_for_ulrs = (
                'SELECT \
                id, \
                name \
                FROM urls \
                ORDER BY urls.id DESC;'
            )
            cursor.execute(query_for_ulrs)
            urls = cursor.fetchall()
            list_of_urls = []

            for row in urls:
                list_of_urls.append(
                    {
                        'id': row.id,
                        'name': row.name
                    }
                )

            query_for_url_checks = (
                'SELECT \
                id, \
                url_id, \
                status_code, \
                created_at \
                FROM url_checks \
                ORDER BY id;'
            )
            cursor.execute(query_for_url_checks)
            urls_checks = cursor.fetchall()

            for row_url in list_of_urls:
                for row_check in urls_checks:
                    if row_url['id'] == row_check.url_id:
                        row_url.update({
                                'last_check': row_check.created_at,
                                'status_code': row_check.status_code 
                        })
            
            self.conn.commit()
            return list_of_urls

    def get_url_by_id(self, id):
        with self.conn.cursor(cursor_factory=NamedTupleCursor) as cursor:
            cursor.execute(
                'SELECT * FROM urls WHERE id = (%s)',
                (id,)
            )
            result = cursor.fetchone()
            return result
        
    def get_url_by_name(self, name):
        with self.conn.cursor(cursor_factory=NamedTupleCursor) as cursor:
            cursor.execute(
                'SELECT * FROM urls WHERE name = (%s)',
                (name,)
            )
            result = cursor.fetchone()
            self.conn.commit()
            return result
        
    def add_url_checks(self, data):
        with self.conn.cursor(cursor_factory=NamedTupleCursor) as cursor:
            cursor.execute(
                'INSERT INTO url_checks \
                (url_id, status_code, h1, title, description) \
                VALUES \
                (%(url_id)s, %(status_code)s, %(h1)s, %(title)s, \
                %(description)s) \
                RETURNING id',
                data
            )
            self.conn.commit()

    def get_url_checks_by_id(self, id):
        with self.conn.cursor(cursor_factory=NamedTupleCursor) as cursor:
            cursor.execute(
                'SELECT * FROM url_checks \
                WHERE url_id = (%s) ORDER BY id DESC',
                (id,)
            )
            result = cursor.fetchall()
            self.conn.commit()
            return result
