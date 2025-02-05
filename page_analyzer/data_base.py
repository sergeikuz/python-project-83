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
            cursor.execute('SELECT * FROM urls')
            result = cursor.fetchall()
            return result


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
