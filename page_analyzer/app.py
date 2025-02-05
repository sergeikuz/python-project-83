import os

from dotenv import load_dotenv
from flask import (
    Flask,
    abort,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

from .data_base import add_url, get_all_urls, get_url_by_id, get_url_by_name
from .normalize_url import normalize_url, validate_url

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
SECRET_KEY = os.getenv('SECRET_KEY')

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['DATABASE_URL'] = DATABASE_URL


@app.route('/')
def index():
    return render_template('index.html')


@app.post('/urls')
def urls_create():
    url = request.form.get('url', '').strip()
    errors = validate_url(url)
    if errors:
        for text, category in errors:
            flash(text, category)
        return render_template('index.html', url=url), 422
    
    url = normalize_url(url)
    found_url = get_url_by_name(DATABASE_URL, url)

    if found_url:
        flash('Страница уже существует', 'info')
        id = found_url.id
        return redirect(url_for('url', id=id))
    else:
        id = add_url(DATABASE_URL, url)
        flash('Страница успешно добавлена', 'success')
        return redirect(url_for('url', id=id.id))
    

@app.get('/urls')
def urls():
    urls = get_all_urls(DATABASE_URL)
    return render_template('urls.html', urls=urls)


@app.get('/urls/<int:id>')
def url(id):
    url = get_url_by_id(DATABASE_URL, id)
    if not url:
        return abort(404)
    
    return render_template(
        'url.html',
        url=url,
    )


@app.errorhandler(404)
def page_not_found(error):
    return render_template('errors/404.html'), 404