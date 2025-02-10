import psycopg2
from psycopg2.extras import NamedTupleCursor


def get_connect(config):
    return psycopg2.connect(config)


def add_url(config, ulr):
    with get_connect(config) as conect:
        with conect.cursor(cursor_factory=NamedTupleCursor) as cursor:
            cursor.execute(
                'INSERT INTO urls (name) VALUES (%s) RETURNING id',
                (str(ulr),)
            )
            result = cursor.fetchone()
            conect.commit()
            return result


def get_all_urls(config):
    with get_connect(config) as conect:
        with conect.cursor(cursor_factory=NamedTupleCursor) as cursor:
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


def get_url_by_id(config, id):
    with get_connect(config) as conect:
        with conect.cursor(cursor_factory=NamedTupleCursor) as cursor:
            cursor.execute(
                'SELECT * FROM urls WHERE id = (%s)',
                (id,)
            )
            result = cursor.fetchone()
            return result
        

def get_url_by_name(config, name):
    with get_connect(config) as conect:
        with conect.cursor(cursor_factory=NamedTupleCursor) as cursor:
            cursor.execute(
                'SELECT * FROM urls WHERE name = (%s)',
                (name,)
            )
            result = cursor.fetchone()
            return result
        

def add_url_checks(config, id, status_code):
    with get_connect(config) as conect:
        with conect.cursor(cursor_factory=NamedTupleCursor) as cursor:
            cursor.execute(
                'INSERT INTO url_checks (url_id, status_code) VALUES (%s, %s) \
                RETURNING id',
                (int(id), int(status_code),)
            )
            conect.commit()


def get_url_checks_by_id(config, id):
    with get_connect(config) as conect:
        with conect.cursor(cursor_factory=NamedTupleCursor) as cursor:
            cursor.execute(
                'SELECT * FROM url_checks \
                WHERE url_id = (%s) ORDER BY id DESC',
                (id,)
            )
            result = cursor.fetchall()
            return result