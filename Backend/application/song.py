#music v2/backend/Mysite/song.py
import os
from operator import or_
from flask import Blueprint,request,jsonify,current_app
from flask_jwt_extended import jwt_required,get_jwt_identity
from werkzeug.utils import secure_filename
from sqlalchemy import func
from datetime import datetime
from .model import Playlist, User,Song,Rating,Album
from . import db

# from .views import creator_required




songs =Blueprint('songs',__name__)




def is_creator(current_user_id):
    admin = User.query.get(current_user_id)
    return admin  and admin.role.name == 'Creator'

def is_admin(current_user_id):
    admin = User.query.get(current_user_id)
    return admin  and admin.role.name == 'Admin'

@songs.route("/create-song", methods=['POST'])
@jwt_required()
def create_song():
    current_user_id = get_jwt_identity()
    if is_creator(current_user_id):
        try:
            current_user_id = get_jwt_identity()
            title = request.form.get('title')
            artist = request.form.get('artist')
            genre = request.form.get('genre')
            lyrics = request.form.get('lyrics')
            file = request.files.get('file')
            album_name = request.form.get('album')

            existing_song = Song.query.filter(
                func.lower(Song.title) == func.lower(title)
            ).first()
            
            if existing_song:
                return jsonify({'message': 'A song with the same title and artist already exists'})
            else:

                if not file:
                    return jsonify({'error': 'File not provided'})
                
                upload_folder =current_app.config['UPLOAD_FOLDER']
                song_upload_folder = os.path.join(upload_folder, 'Song')
                    
                if 'file' in request.files:
                    song_data = request.files["file"]
                    timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
                    filename = f"{secure_filename(song_data.filename)}_{timestamp}"
                    filepath = os.path.join(song_upload_folder, filename)
                    song_data.save(filepath)

                if album_name:
                    album = Album.query.filter(func.lower(Album.name) == func.lower(album_name)).first()
                    if not album:
                        new_album = Album(
                            name=album_name,
                            user_id=current_user_id
                        )
                        db.session.add(new_album)
                        db.session.commit()
                        album_id = new_album.id
                    else:
                        album_id = album.id

                song = Song(
                    title=title,
                    artist=artist,
                    genre=genre,
                    lyrics=lyrics,
                    file=filepath,
                    album_id=album_id,
                    author=current_user_id 
                )
    
                song.calculate_duration()
                db.session.add(song)
                db.session.commit()

                new_album1 = Album.query.get(album_id)
                if not new_album1:
                    return jsonify({'error': 'Album not found'})
                song.album = new_album1
                db.session.commit()

                return jsonify({'message': 'Song created successfully'})

        except Exception as e:
            print(e)
            return jsonify({'message': 'Failed to create song'})    


@songs.route('/edit_song/<int:song_id>', methods=['GET', 'POST'])
@jwt_required()
def edit_song(song_id):
    current_user_id = get_jwt_identity()
    
    if is_creator(current_user_id):
        song = Song.query.get(song_id)

        if not song:
            return jsonify({'error': 'Song not found'})
        
        if request.method == 'GET':
            # Return song details
            return jsonify({
                'title': song.title,
                'artist': song.artist,
                'genre': song.genre,
                'album': song.album.name if song.album else None,
                'lyrics': song.lyrics
                # Add other song details as needed
            })
        
        elif request.method == 'POST':
            title = request.form.get('title')
            artist = request.form.get('artist')
            genre = request.form.get('genre')
            lyrics = request.form.get('lyrics')
            file = request.files.get('file')
            album_name = request.form.get('album')

            existing_song = Song.query.filter(
                func.lower(Song.title) == func.lower(title),
                Song.id != song_id
            ).first()
            
            if existing_song:
                return jsonify({'message': 'A song with the same title and artist already exists'})
            else:

                if album_name:
                    album = Album.query.filter(func.lower(Album.name) == func.lower(album_name)).first()
                    if not album:
                        new_album = Album(
                            name=album_name,
                            user_id=current_user_id
                        )
                        db.session.add(new_album)
                        db.session.commit()
                        album_id = new_album.id
                    else:
                        album_id = album.id
                upload_folder =current_app.config['UPLOAD_FOLDER']
                song_upload_folder = os.path.join(upload_folder, 'Song')

                if file:
                    if song.file:
                        
                        try:
                            os.remove(song.file)
                        except OSError as e:
                            print(f"Error deleting old file: {e}")
                    
                    song_data = request.files["file"]
                    timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
                    filename = f"{secure_filename(song_data.filename)}_{timestamp}"
                    filepath = os.path.join(song_upload_folder, filename)
                    song_data.save(filepath)
                else:
                    # Use the old file path
                    filepath = song.file

                new_album1 = Album.query.get(album_id)
                
                if not new_album1:
                    return jsonify({'error': 'Album not found'})

                song.title=title
                song.artist=artist
                song.genre=genre
                song.lyrics=lyrics
                song.file=filepath
                song.album_id=album_id
                song.author=current_user_id 
                
               
    
                song.calculate_duration()
                
                db.session.commit()

                song.album = new_album1
                db.session.commit()
                return jsonify({'message': 'Song updated successfully'})
        
    else:
        return jsonify({'message': 'Access forbidden'})


@songs.route("/add-to-album-song/<int:song_id>", methods=['POST'])
@jwt_required()
def add_to_album_song(song_id):
    current_user_id = get_jwt_identity()
    if is_creator(current_user_id):
            new_album_id = request.json.get('new_album_id')

            # Check if the user is authorized to perform this action
            song = Song.query.filter_by(id=song_id, author=current_user_id).first()
            if not song:
                return jsonify({'error': 'Song not found or unauthorized access'})

            # Retrieve the new album
            new_album = Album.query.get(new_album_id)
            if not new_album:
                return jsonify({'error': 'Album not found'})

            # Update the album of the song
            song.album = new_album
            db.session.commit()

            return jsonify({'message': 'Song album updated successfully'})
    else:
        return jsonify({'message': 'Not allowed'})



@songs.route('/delete-song/<int:song_id>', methods=['DELETE'])
@jwt_required()
def delete_song(song_id):
    current_user_id = get_jwt_identity()
    if is_creator(current_user_id) or is_admin(current_user_id):
        song = Song.query.get(song_id)

        if song:
            Rating.query.filter_by(song_id=song_id).delete()
            db.session.commit()
            
            if song.file :
                try:
                    os.remove( song.file)
                except OSError as e:
                    print(f"Error deleting image file: {e}")

            db.session.delete(song)
            db.session.commit()
            return jsonify({'message': 'song removed successfully'})
        else:
            return jsonify({'error': 'song not found'})
    else:
        return jsonify({'message': 'Access forbidden'})
    


@songs.route('/rate-song', methods=['POST'])
@jwt_required()
def rate_song():
    current_user_id = get_jwt_identity()
    try:
        data = request.json
        song_id = data.get('song_id')
        value = data.get('value')

        if not song_id or not value:
            return jsonify({'message': 'Song ID and rating value are required'})
        existing_rating = Rating.query.filter_by(song_id=song_id, user_id=current_user_id).first()
        if existing_rating:
            existing_rating.value = value
            db.session.commit()
            return jsonify({'message': 'Rating updated successfully'})
        else:
            rating = Rating(song_id=song_id, value=value,user_id=current_user_id)
            db.session.add(rating)
            db.session.commit()

            return jsonify({'message': 'Rating submitted successfully'})
    except Exception as e:
        return jsonify({'message': 'Failed to submit rating', 'error': str(e)})
