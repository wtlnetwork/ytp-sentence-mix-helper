import os

basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'thomas_subtitles.db')

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', f'sqlite:///{db_path}?mode=ro')
    SQLALCHEMY_TRACK_MODIFICATIONS = False