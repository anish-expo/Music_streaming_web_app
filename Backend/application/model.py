#music v2/backend/Mysite/model.py
from . import db

from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash
import mutagen

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)

    def __repr__(self):
        return f'<Role {self.name}>'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(255), default='default.jpg')
    name =db.Column(db.Text,nullable=False)
    email =db.Column(db.String(150),unique=True)
    username =db.Column(db.String(150),unique=True,nullable=False)
    password =db.Column(db.String(150))
    date_created = db.Column(db.DateTime(timezone=True),default=func.now())
    Song = db.relationship("Song",backref="user",passive_deletes=True,cascade="all, delete-orphan")
    playlists = db.relationship('Playlist', back_populates='user',cascade="all, delete-orphan")
    album=db.relationship("Album",back_populates='user',cascade="all, delete-orphan")
    ratings = db.relationship("Rating", back_populates="user",cascade="all, delete-orphan")
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    role = db.relationship('Role', backref=db.backref('users', lazy=True))
    last_login = db.Column(db.DateTime(timezone=True), default=None)

    def __repr__(self):
        return f'<User {self.username}>'
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def is_user(self):
        return self.role.name == 'User'
    def is_creator(self):
        return self.role.name == 'Creator'
    

class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    artist = db.Column(db.String(255), nullable=False)
    duration = db.Column(db.String(20), nullable=False)
    genre = db.Column(db.String(100), nullable=True)
    lyrics = db.Column(db.String(1000), nullable=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    file = db.Column(db.String(255), nullable=False)  
    author = db.Column(db.Integer,db.ForeignKey("user.id",ondelete="CASCADE"),nullable=False)
    ratings = db.relationship('Rating', back_populates='song') 
    album_id = db.Column(db.Integer, db.ForeignKey('album.id'))
    album = db.relationship('Album', back_populates='songs')
    flagged = db.Column(db.Boolean, default=False)
    play_count = db.Column(db.Integer, default=0)

    def calculate_duration(self):
        try:
            audio = mutagen.File(self.file)
            duration_seconds = int(audio.info.length)
            minutes = duration_seconds // 60
            seconds = duration_seconds % 60
            self.duration = f"{minutes}:{seconds:02}"
        except Exception as e:
            print(f"Error calculating duration: {e}")
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'artist': self.artist,
            'duration': self.duration,
            'genre': self.genre,
            'lyrics': self.lyrics,
            'date_created': self.date_created.strftime('%Y-%m-%d %H:%M:%S'),  # Format date as string
            'file': self.file,
            'author': self.author,
            'album_id': self.album_id
            
        }

class Playlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    description = db.Column(db.Text, nullable=True)
    songs = db.relationship('Song', secondary='playlist_song', backref='playlists')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id',ondelete="CASCADE"))
    user = db.relationship('User', back_populates='playlists')
    



playlist_song = db.Table('playlist_song',
    db.Column('playlist_id', db.Integer, db.ForeignKey('playlist.id')),
    db.Column('song_id', db.Integer, db.ForeignKey('song.id'))
)


class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    artist= db.Column(db.Text, nullable=True)
    image = db.Column(db.String(255), default='default.jpg')
    genre = db.Column(db.Text,nullable=True)
    songs = db.relationship('Song', secondary='album_song', back_populates='album')
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id',ondelete="CASCADE"))
    user = db.relationship('User', back_populates='album')
    ratings = db.relationship('Rating', back_populates='album')
    flagged = db.Column(db.Boolean, default=False)
 
album_song = db.Table('album_song',
    db.Column('album_id', db.Integer, db.ForeignKey('album.id')),
    db.Column('song_id', db.Integer, db.ForeignKey('song.id'))
)




class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer)  
    user_id = db.Column(db.Integer, db.ForeignKey('user.id',ondelete="CASCADE"), nullable=False)
    user = db.relationship('User', back_populates='ratings',)

    song_id = db.Column(db.Integer, db.ForeignKey('song.id',ondelete="CASCADE"), nullable=True)
    song = db.relationship('Song', back_populates='ratings') 

    album_id = db.Column(db.Integer, db.ForeignKey('album.id',ondelete="CASCADE"),nullable=True)
    album = db.relationship('Album', back_populates='ratings')