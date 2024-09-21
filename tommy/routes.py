import string

from flask import Blueprint, render_template, request
from .models import Subtitle
from sqlalchemy import func

main = Blueprint('main', __name__)

# Mapping of full names to narrator keys (reversed for lookup)
narrators = {
    "Any": None,
    "Ringo Starr": "ringo",
    "Michael Angelis": "angelis",
    "George Carlin": "carlin",
    "Alec Baldwin": "baldwin",
    "Michael Brandon": "brandon"
}

# Create a reversed dictionary for looking up full names by key
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

        # Normalize the query to remove punctuation and make it lowercase
        normalized_query = normalize_text(query)

        # Build the search query
        search_filter = func.lower(func.replace(Subtitle.line, string.punctuation, '')).contains(normalized_query)  # Case-insensitive and ignoring punctuation

        # Check if 'narrator' is None or empty string, and build the filter accordingly
        if narrator in [None, '', 'None']:
            narrator_filter = True  # No filter for narrator, allow any
        else:
            narrator_filter = Subtitle.narrator == narrator

        # Execute the query in read-only mode
        results = Subtitle.query.filter(search_filter).filter(narrator_filter).order_by(
            Subtitle.series, Subtitle.episode_number).all()

    return render_template('index.html', narrators=narrators, narrator_lookup=narrator_lookup, results=results, query=query, selected_narrator=narrator)