from . import db

class Subtitle(db.Model):
    __tablename__ = 'subtitles'

    id = db.Column(db.Integer, primary_key=True)
    series = db.Column(db.Integer)
    episode_number = db.Column(db.Integer)
    episode_title = db.Column(db.String(255))
    region = db.Column(db.String(8))
    narrator = db.Column(db.String(255))
    start_time = db.Column(db.String(8))
    end_time = db.Column(db.String(8))
    line = db.Column(db.Text)

    def __repr__(self):
        return f'<Subtitle {self.episode_title}>'
