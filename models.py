from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Video(db.Model):
    __tablename__ = 'video'
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(120), nullable=False)
    title = db.Column(db.String(120), nullable=True)

    def __repr__(self):
        return f'<Video {self.title}>'
