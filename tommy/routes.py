import string

from flask import Blueprint, render_template, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import cross_origin
from .models import Subtitle
from sqlalchemy import func

main = Blueprint('main', __name__)

narrators = {
    "Any": None,
    "Ringo Starr": "ringo",
    "Michael Angelis": "angelis",
    "George Carlin": "carlin",
    "Alec Baldwin": "baldwin",
    "Michael Brandon": "brandon"
}

narrator_lookup = {v: k for k, v in narrators.items() if v is not None}

def normalize_text(text):
    return ''.join(char for char in text if char not in string.punctuation).lower()

@main.route('/', methods=['GET', 'POST'])
def index():
    query = ''
    narrator = None
    results = []

    if request.method == 'POST':
        query = request.form['query']
        narrator = request.form['narrator']

        if query.strip():
            normalized_query = normalize_text(query)

            search_filter = func.lower(func.replace(Subtitle.line, string.punctuation, '')).contains(normalized_query)  # Case-insensitive and ignoring punctuation

            if narrator in [None, '', 'None']:
                narrator_filter = True  # No filter for narrator, allow any
            else:
                narrator_filter = Subtitle.narrator == narrator

            results = Subtitle.query.filter(search_filter).filter(narrator_filter).order_by(
                Subtitle.series, Subtitle.episode_number).all()
        else:
            results = []

    return render_template('index.html', narrators=narrators, narrator_lookup=narrator_lookup, results=results, query=query, selected_narrator=narrator)

limiter = Limiter(get_remote_address)

@main.route('/api/find_line', methods=['GET'])
@cross_origin(origins='*')
@limiter.limit("120 per minute")
def api_search():
    query = request.args.get('query', '')
    narrator = request.args.get('narrator', None)
    results = []

    if query.strip():
        normalized_query = normalize_text(query)
        search_filter = func.lower(func.replace(Subtitle.line, string.punctuation, '')).contains(normalized_query)

        if narrator in [None, '', 'None']:
            narrator_filter = True
        else:
            narrator_filter = Subtitle.narrator == narrator

        results = Subtitle.query.filter(search_filter).filter(narrator_filter).order_by(
            Subtitle.series, Subtitle.episode_number).all()

    response_data = [
        {
            'series': result.series,
            'episode_number': result.episode_number,
            'episode_title': result.episode_title,
            'region': result.region.upper(),
            'narrator': narrator_lookup.get(result.narrator, result.narrator),
            'line': result.line,
            'start_time': result.start_time,
            'end_time': result.end_time
        }
        for result in results
    ]

    return jsonify(response_data)