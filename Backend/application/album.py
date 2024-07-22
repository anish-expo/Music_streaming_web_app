#music v2/backend/Mysite/album.py

import os
from flask import Blueprint,request,flash,jsonify,current_app
from flask_jwt_extended import jwt_required,get_jwt_identity
from datetime import datetime
from werkzeug.utils import secure_filename
from .model import User,Song,Rating,Album,album_song
from . import db


album = Blueprint('album',__name__)





def is_creator(current_user_id):
    admin = User.query.get(current_user_id)
    return admin  and admin.role.name == 'Creator'

def is_admin(current_user_id):
    admin = User.query.get(current_user_id)
    return admin  and admin.role.name == 'Admin'

@album.route('/create_album', methods=['POST'])
@jwt_required()
def create_album():
    current_user_id = get_jwt_identity()
    if is_creator(current_user_id):
        try:
            name = request.form.get('name')
            artist =request.form.get('artist')
            genre = request.form.get('genre')
            existing_album = Album.query.filter_by(name=name).first()
            if existing_album:
                return jsonify({'message': 'An album with the same name already exists'})
            else:

                upload_folder =current_app.config['UPLOAD_FOLDER']
                song_upload_folder = os.path.join(upload_folder, 'Song')
                
                if 'image' in request.files:
                    image_data = request.files["image"]
                    timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
                    filename = f"{secure_filename(image_data.filename)}_{timestamp}"
                    filepath = os.path.join(song_upload_folder, filename)
                    image_data.save(filepath)
                else:
                    # If no image data is provided, set the default image
                    filepath = 'default.jpg'
                
                new_album = Album(
                    name=name,
                    artist=artist,
                    genre=genre,
                    image=filepath,
                    user_id=current_user_id 
                )

                # Add the new album to the database session
                db.session.add(new_album)
                db.session.commit()

                # Return a success response
                return jsonify({'message': 'Album created successfully'})
        except Exception as e:
                # Handle any errors that may occur
                print(e)
                return jsonify({'error': 'Failed to create album'})
        
    else:
        return jsonify({"msg": "Access forbidden"})

@album.route('/remove_album/<int:album_id>', methods=['DELETE'])
@jwt_required()
def remove_album(album_id):
    current_user_id = get_jwt_identity()
    if is_creator(current_user_id) or is_admin(current_user_id):
        album = Album.query.get(album_id)

        if album:
            Rating.query.filter_by(album_id=album.id).delete()
            for song in album.songs:
                song.album_id = None
            if album.image and album.image != 'default.jpg':
                
                    try:
                        os.remove( album.image)
                    except OSError as e:
                        print(f"Error deleting image file: {e}")

            db.session.delete(album)
            db.session.commit()
            return jsonify({'message': 'Album removed successfully'})
        else:
            return jsonify({'error': 'Album not found'})
    else:
        return jsonify({'error': 'Access forbidden'})
    

@album.route('/edit_album/<int:album_id>',methods= ['GET','POST'])
@jwt_required()
def edit_album(album_id):
    current_user_id = get_jwt_identity()
    if is_creator(current_user_id):
        album = Album.query.get(album_id)

        if not album:
            return jsonify({'error': 'Song not found'})
        
        if request.method == 'GET':
            # Return song details
            return jsonify({
                'name': album.name,
                'artist': album.artist,
                'genre': album.genre,
                
            })
        elif request.method == 'POST':
            name = request.form.get('name')
            artist = request.form.get('artist')
            genre = request.form.get('genre')

            existing_album = Album.query.filter(Album.name == name, Album.id != album_id).first()
    
            if existing_album:
                return jsonify({'message': 'A album with the same title and artist already exists'})
            else:

                upload_folder =current_app.config['UPLOAD_FOLDER']
                song_upload_folder = os.path.join(upload_folder, 'Song')

                if 'image' in request.files:
                    if album.image != 'default.jpg':
                        
                        try:
                            os.remove(album.image)
                        except OSError as e:
                            print(f"Error deleting old file: {e}")
                    image_data = request.files["image"]
                    timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
                    filename = f"{secure_filename(image_data.filename)}_{timestamp}"
                    filepath = os.path.join(song_upload_folder, filename)
                    image_data.save(filepath)
                else:
                    
                    filepath = album.image
                    
                album.name = name
                album.artist = artist
                album.genre = genre
                album.image = filepath
                db.session.commit()
                return jsonify({'message': 'album edited successfully'})
        
    else:
        return jsonify({'message': 'Access forbidden'})

@album.route('/get_album_song/<int:album_id>',methods= ['GET'])
@jwt_required()
def get_album_song(album_id): 
    album = Album.query.get(album_id)
    if not album:
        return jsonify({'message': 'Album not found'})

    # songs = album.songs
    songs = Song.query.filter_by(album_id=album_id).all()
    serialized_songs = []
    for song in songs:
        if song.flagged:
            continue
        ratings = [rating.value for rating in song.ratings]
        average_rating = sum(ratings) / len(ratings) if ratings else 0
        serialized_song = {
            'id': song.id,
            'title': song.title,
            'artist': song.artist,
            'duration': song.duration,
            'genre': song.genre,
            'lyrics': song.lyrics,
            'date_created': song.date_created,
            'songfile': song.file,
            'author': song.author,
            'album_id': song.album_id,
            'average_rating': average_rating,
            'play_count': song.play_count
        }
        serialized_songs.append(serialized_song)

    
    return jsonify({'album_name': album.name, 'songs': serialized_songs})

@album.route('/remove-song-from-album/<int:song_id>/<int:album_id>', methods=['DELETE'])
@jwt_required()
def remove_song(song_id, album_id):
    current_user_id = get_jwt_identity()
    if is_creator(current_user_id):
    
        song = Song.query.get(song_id)
        album = Album.query.get(album_id)
        # print(song.album_id)
        
        if not song or not album:
            return jsonify({'error': 'Song or album not found'})
        
        if song.album_id != album.id:
            return jsonify({'error': 'The album does not contain the specified song'})

        
        # Remove the song from the album
        album.songs.remove(song)
        db.session.commit()
        
        return jsonify({'message': 'Song removed from the album successfully refresh the page'})
    else:
        return jsonify({'message': 'Access forbiden'})


@album.route('/rate-album', methods=['POST'])
@jwt_required()
def rate_album():
    current_user_id = get_jwt_identity()
    try:
        data = request.json
        album_id = data.get('album_id')
        value = data.get('value')

        if not album_id or not value:
            return jsonify({'message': 'Song ID and rating value are required'})
        
        existing_rating = Rating.query.filter_by(album_id=album_id, user_id=current_user_id).first()
        if existing_rating:
            existing_rating.value = value
            db.session.commit()
            return jsonify({'message': 'Rating updated successfully'})
        else:
            rating = Rating(album_id=album_id, value=value, user_id=current_user_id)
            db.session.add(rating)
            db.session.commit()
            return jsonify({'message': 'Rating submitted successfully'})

        
    except Exception as e:
        return jsonify({'message': 'Failed to submit rating', 'error': str(e)})
