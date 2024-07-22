#music v2/backend/Mysite/playlist.py

from flask import Blueprint,jsonify,request
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required,get_jwt_identity
from .model import Playlist, User,Song,Rating,playlist_song
from . import db

# from .views import user_required
playlist = Blueprint('playlist',__name__)
 
# ...........................................................................................playlist........................................................................
@playlist.route('/create_playlist', methods=['POST'])
@jwt_required()
def create_playlist():
    current_user_id = get_jwt_identity()
    try:
        # Get data from the request
        data = request.get_json()
        name = data.get('name')
        description = data.get('description')
        
        if not name:
            return jsonify({'message': 'Playlist name is required'})
        
        existing_playlist = Playlist.query.filter_by(name=name, user_id=current_user_id).first()
        if existing_playlist:
            return jsonify({'message': 'Playlist with the same name already exists for the current user'})
        
        # Create the playlist
        new_playlist = Playlist(
            name=name,
            description=description,
            user_id=current_user_id  
        )
        
        # Add the playlist to the database
        db.session.add(new_playlist)
        db.session.commit()
        
        return jsonify({'message': 'Playlist created successfully'})
    except Exception as e:
        return jsonify({'message': 'Failed to create playlist', 'error': str(e)})
    
@playlist.route('/getplaylists', methods=['GET'])
@jwt_required()
def get_playlists():
    try:
        current_user_id = get_jwt_identity()
        playlists = Playlist.query.filter_by(user_id=current_user_id).all()

       
        serialized_playlists = [{
            'id': playlist.id,
            'name': playlist.name,
            'description': playlist.description,
            'date_created': playlist.date_created,
            'songs': [song.serialize() for song in playlist.songs]
            
        } for playlist in playlists]

        # Return the serialized playlists as JSON response
        return jsonify({'playlists': serialized_playlists})
    except Exception as e:
        return jsonify({'message': 'Failed to fetch playlists', 'error': str(e)})

@playlist.route('/add_to_playlist', methods=['POST'])
@jwt_required()
def add_to_playlist():
    try:
        current_user_id = get_jwt_identity()

        data = request.get_json()
        song_id = data.get('song_id')
        playlist_id = data.get('playlist_id')
        new_playlist_name = data.get('new_playlist_name')

        if not playlist_id and not new_playlist_name:
            return jsonify({'message': 'Please provide a playlist ID or a new playlist name'})

        song = Song.query.get(song_id)
        if not song:
            return jsonify({'message': 'Song not found'})

        user_playlist = None
        if playlist_id:
            user_playlist = Playlist.query.filter_by(id=playlist_id, user_id=current_user_id).first()
        elif new_playlist_name:
            user_playlist = Playlist(name=new_playlist_name, user_id=current_user_id)
            db.session.add(user_playlist)
            db.session.commit()

        if not user_playlist:
            return jsonify({'message': 'Playlist not found or unauthorized'})

        
        user_playlist.songs.append(song)
        db.session.commit()

        return jsonify({'message': 'Song added to playlist successfully'})

    except Exception as e:
        return jsonify({'message': 'Failed to add song to playlist', 'error': str(e)})


@playlist.route('/get_playlist_song/<int:playlist_id>',methods= ['GET'])
@jwt_required()
def get_album_song(playlist_id): 
    album = Playlist.query.get(playlist_id)
    if not album:
        return jsonify({'message': 'Album not found'})

    # songs = album.songs
    songs = Song.query.join(playlist_song).filter(playlist_song.c.playlist_id == playlist_id).all()
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
            'play_count':song.play_count
        }
        serialized_songs.append(serialized_song)

    
    return jsonify({'playlist_name': playlist.name, 'songs': serialized_songs})


@playlist.route('/remove-song-from-playlist/<int:song_id>/<int:playlist_id>', methods=['DELETE'])
@jwt_required()
def remove_song(song_id, playlist_id):
    try:
        current_user_id = get_jwt_identity()
        playlist = Playlist.query.filter_by(id=playlist_id, user_id=current_user_id).first()
        if not playlist:
            return jsonify({'message': 'Playlist not found or unauthorized'})
            
            # Query the song to ensure it exists
        song = Song.query.get(song_id)
        if not song:
            return jsonify({'message': 'Song not found'})
            
           
        playlist.songs.remove(song)
        db.session.commit()
            
        return jsonify({'message': 'Song removed from playlist successfully'})
    except Exception as e:
        return jsonify({'message': 'Failed to remove song from playlist', 'error': str(e)})
        
   


@playlist.route('/remove_playlist/<int:playlist_id>', methods=['DELETE'])
@jwt_required()
def remove_playlist(playlist_id):
    try:
        current_user_id = get_jwt_identity()
        
        playlist = Playlist.query.filter_by(id=playlist_id, user_id=current_user_id).first()
       
        if not playlist:
            return jsonify({'message': 'Playlist not found or unauthorized'})
        
      
        db.session.delete(playlist)
        db.session.commit()
        
        return jsonify({'message': 'Playlist removed successfully'})
        
    except Exception as e:
        return jsonify({'message': 'Failed to remove playlist', 'error': str(e)})
    

    

