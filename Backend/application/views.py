#music v2/backend/Mysite/views.py

from operator import or_
from flask import Blueprint,request,jsonify,current_app,send_from_directory
from sqlalchemy import func
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required,get_jwt_identity
from .model import Playlist, User,Song,Rating,Album,Role
from . import db

import time
from functools import wraps
from flask import abort
import os
from application import cache

import logging

views =Blueprint("views",__name__)





@views.route("/home")
def home():
    allalbums = Album.query.all()
    serialized_allalbums = []
    for album in allalbums:
        if album.flagged:
            continue
        ratings = Rating.query.filter_by(album_id=album.id).all()
        total_rating = sum(rating.value for rating in ratings)
        total_ratings = len(ratings)
        average_rating = total_rating / total_ratings if total_ratings != 0 else 0
        serialized_album = {
                'id': album.id,
                'name': album.name,
                'artist': album.artist,
                'image': album.image,
                'genre': album.genre,
                'songs': [song.serialize() for song in album.songs] ,
                'average_rating': average_rating, 
                'flagged':album.flagged
            }

        serialized_allalbums.append(serialized_album)

    allsongs = Song.query.all()
    serialized_allsongs = []
    for song in allsongs:
        ratings = Rating.query.filter_by(song_id=song.id).all()
        total_rating = sum(rating.value for rating in ratings)
        average_rating = total_rating / len(ratings) if ratings else 0
        serialized_song = {
                'id': song.id,
                'title': song.title,
                'artist': song.artist,
                'duration': song.duration,
                'genre': song.genre,
                'album': song.album.name if song.album else "No Album",
                'lyrics': song.lyrics,
                'songfile': song.file,
                'average_rating': average_rating , 
                'flagged': song.flagged,
                'play_count':song.play_count
            }

        serialized_allsongs.append(serialized_song)
    return jsonify({
            'allalbum': serialized_allalbums,
            'allsong': serialized_allsongs
        })    

      
@views.route('/show/<filename>', methods=['GET'])
def show(filename):
    # app_root = os.path.dirname(os.path.abspath(__file__))
    app_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # print('approot:',app_root)
    file_path = os.path.join(app_root, 'static', 'upload','User', filename)
    # print('file path:', file_path)

    if os.path.exists(file_path):
        return send_from_directory(os.path.join(app_root, 'static', 'upload', 'User'), filename)
    else:
        # print('File not found:', filename)
        return 'File not found'
    
@views.route('/showsong/<filename>', methods=['GET'])
def showsong(filename):
    # app_root = os.path.dirname(os.path.abspath(__file__))
    app_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # print('approot:',app_root)
    file_path = os.path.join(app_root, 'static', 'upload','Song', filename)
    # print('file path:', file_path)

    if os.path.exists(file_path):
        return send_from_directory(os.path.join(app_root, 'static', 'upload', 'Song'), filename)
    else:
        # print('File not found:', filename)
        return 'File not found'
    

@views.route('/playsong/<int:song_id>/<filename>', methods=['GET'])
def playsong(song_id,filename):
    # app_root = os.path.dirname(os.path.abspath(__file__))
    app_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # print('approot:',app_root)
    file_path = os.path.join(app_root, 'static', 'upload','Song', filename)
    # print('file path:', file_path)

    song = Song.query.get(song_id)
    if song:
        song.play_count += 1
        db.session.commit()    

    if os.path.exists(file_path):
        return send_from_directory(os.path.join(app_root, 'static', 'upload', 'Song'), filename)
    else:
        # print('File not found:', filename)
        return 'File not found'
    

# ...................................................................................admin...................................................................................
def is_admin(current_user_id):
    admin = User.query.get(current_user_id)
    return admin  and admin.role.name == 'Admin'
    

@views.route('/admin_dashboard/<username>', methods=['GET'])
@jwt_required()
@cache.cached(timeout=20)
def admin_dashboard(username):
    current_user_id = get_jwt_identity()
    # print(is_admin(current_user_id))
    if  is_admin(current_user_id):
            total_users = User.query.count()
            total_creators = User.query.join(Role).filter(Role.name == 'Creator').count()
            total_normal_user= User.query.join(Role).filter(Role.name == 'User').count()
            total_albums = Album.query.count()
            total_song = Song.query.count()
            
            user =  User.query.get(current_user_id)
            user_info = {
                    'id': user.id,
                    'name':user.name,
                    'username': user.username,
                    'email': user.email,
                    'image':user.image
                }
           

            return jsonify({
                'user':user_info,
                'total_users': total_users -1,
                'total_creators': total_creators,
                'total_albums': total_albums,
                'total_normal_user':total_normal_user,
                'total_song':total_song
                

            })
    else:
        return jsonify({"msg": "Access forbidden"})
    
@views.route('/allalbum',methods =['GET'])
@jwt_required()
def fetchalbum():
    current_user_id = get_jwt_identity()
    if  is_admin(current_user_id):
        allalbums = Album.query.all()
        serialized_allalbums = []
        for album in allalbums:
            ratings = Rating.query.filter_by(album_id=album.id).all()
            total_rating = sum(rating.value for rating in ratings)
            total_ratings = len(ratings)
            average_rating = total_rating / total_ratings if total_ratings != 0 else 0
            serialized_album = {
                'id': album.id,
                'name': album.name,
                'artist': album.artist,
                'image': album.image,
                'genre': album.genre,
                'user_id': album.user_id,
                'user': album.user.name,
                'average_rating': average_rating, 
                'flagged':album.flagged
            }

            serialized_allalbums.append(serialized_album)
        return jsonify({
            'allalbum': serialized_allalbums
        })    

    else:
        return jsonify({"msg": "Access forbidden"})
    
@views.route('/allsong',methods =['GET'])
@jwt_required()
def fetchallsong():
    current_user_id = get_jwt_identity()
    if  is_admin(current_user_id):    
        allsongs = Song.query.all()
        serialized_allsongs = []
        for song in allsongs:
            ratings = Rating.query.filter_by(song_id=song.id).all()
            total_rating = sum(rating.value for rating in ratings)
            average_rating = total_rating / len(ratings) if ratings else 0
            serialized_song = {
                'id': song.id,
                'title': song.title,
                'artist': song.artist,
                'duration': song.duration,
                'genre': song.genre,
                'album': song.album.name if song.album else "No Album",
                'lyrics': song.lyrics,
                'songfile': song.file,
                'average_rating': average_rating , 
                'flagged': song.flagged,
                'play_count':song.play_count
            }

            serialized_allsongs.append(serialized_song)
        return jsonify({
            'allsong': serialized_allsongs
        })    

    else:
        return jsonify({"msg": "Access forbidden"})    



@views.route('/get_album_song_admin/<int:album_id>',methods= ['GET'])
@jwt_required()
def get_album_song(album_id): 
    current_user_id = get_jwt_identity()
    if  is_admin(current_user_id):
        album = Album.query.get(album_id)
        if not album:
            return jsonify({'message': 'Album not found'})

        # songs = album.songs
        songs = Song.query.filter_by(album_id=album_id).all()
        serialized_songs = []
        for song in songs:
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
                'flagged': song.flagged,
                'play_count':song.play_count
            }
            serialized_songs.append(serialized_song)

        
        return jsonify({'album_name': album.name, 'songs': serialized_songs})
    
    else:
        return jsonify({"msg": "Access forbidden"})

@views.route('/flag-album/<int:album_id>', methods=['PUT'])
@jwt_required()
def toggle_album_flag(album_id):
    current_user_id = get_jwt_identity()
    if  is_admin(current_user_id):
        try:
            # Find the album by ID
            album = Album.query.get(album_id)
            if not album:
                return jsonify({'error': 'Album not found'})

            album.flagged = not album.flagged
            for song in album.songs:
               song.flagged = album.flagged
            db.session.commit()

            return jsonify({'message': 'Flag status updated successfully', 'flagged': album.flagged})
        except Exception as e:
            return jsonify({'error': str(e)})

@views.route('/flag-song/<int:song_id>', methods=['PUT'])
@jwt_required()
def toggle_song_flag(song_id):
    current_user_id = get_jwt_identity()
    if  is_admin(current_user_id):
        try:
            # Find the album by ID
            song = Song.query.get(song_id)
            if not song:
                return jsonify({'error': 'Album not found'})

            song.flagged = not song.flagged
            
            db.session.commit()

            return jsonify({'message': 'Flag status updated successfully', 'flagged': song.flagged})
        except Exception as e:
            return jsonify({'error': str(e)})

# ...........................................................................................user......................................................................................


def is_user(current_user_id):
    admin = User.query.get(current_user_id)
    return admin  and admin.role.name == 'User'

@views.route('user_dashbord/<username>',methods=['GET'])
@jwt_required()
def user_dashbord(username):
    current_user_id = get_jwt_identity()
    if is_user(current_user_id):
        user= User.query.get(current_user_id)

        # Fetch user's playlists
        playlists = Playlist.query.filter_by(user_id=user.id).all()

        # Serialize playlists
        serialized_playlists = []
        for playlist in playlists:
            serialized_playlist = {
                'id': playlist.id,
                'name': playlist.name,
                'description': playlist.description,
                
                'song_count': len(playlist.songs)
               
            }
            serialized_playlists.append(serialized_playlist)

        # Fetch all songs
        songs = Song.query.all()

        # Serialize songs
        serialized_songs = []
        for song in songs:
            if song.flagged:
                continue
            ratings = [rating.value for rating in song.ratings]

            # Calculate average rating
            average_rating = sum(ratings) / len(ratings) if ratings else 0

            serialized_song = {
                'id': song.id,
                'title': song.title,
                'artist': song.artist,
                'duration': song.duration,
                'genre': song.genre,
                'songfile': song.file,
                'average_rating': average_rating,
                'play_count': song.play_count  
            }
            serialized_songs.append(serialized_song)

        # Fetch all albums
        albums = Album.query.all()

        # Serialize albums
        serialized_albums = []
        for album in albums:
            if album.flagged:
                continue
            average_rating = db.session.query(func.avg(Rating.value)).filter_by(album_id=album.id).scalar()

            if average_rating is None:
                average_rating = 0
            serialized_album = {
                'id': album.id,
                'name': album.name,
                'artist': album.artist,
                'image': album.image,
                'genre': album.genre,
                'song_count': len(album.songs),
                'average_rating': average_rating
            }
            serialized_albums.append(serialized_album)

        return jsonify({
            'user': {
                'id': user.id,
                'username': user.username,
                'name': user.name,
                'email': user.email,
                'image':user.image
                # Add more user data if needed
            },
            'playlists': serialized_playlists,
            'songs': serialized_songs,
            'albums': serialized_albums
        })
    else:
        return jsonify({"msg": "Access forbidden"})
    

@views.route('/make_creator/<int:user_id>', methods=['POST'])
def make_creator(user_id):
    # Find the user by user_id
    user = User.query.get(user_id)

    if not user:
        return jsonify({'message': 'User not found'})

    # Assuming 'Creator' is the name of the role for creators
    creator_role = Role.query.filter_by(name='Creator').first()

    # Update the user's role to be a creator
    user.role = creator_role
    user.is_creator = True

    # Commit changes to the database
    db.session.commit()

    return jsonify({'message': 'User updated to creator successfully'})








#.........................................creator......................................................

def is_creator(current_user_id):
    admin = User.query.get(current_user_id)
    return admin  and admin.role.name == 'Creator'

@views.route('creator_dashbord/<username>',methods=['Get'])
@jwt_required()
def creator_dashbord(username):
    current_user_id = get_jwt_identity()
    if is_creator(current_user_id):
        creator= User.query.get(current_user_id)

        playlists = Playlist.query.filter_by(user_id=creator.id).all()

        # Serialize playlists
        serialized_playlists = []
        for playlist in playlists:
            serialized_playlist = {
                'id': playlist.id,
                'name': playlist.name,
                'description': playlist.description,
                'song_count': len(playlist.songs)
                # You can add more fields as needed
            }
            serialized_playlists.append(serialized_playlist)
        
        creator_songs = Song.query.filter_by(author=creator.id).all()
        serialized_songs=[]
        for songs in creator_songs:
            if songs.flagged:
                continue
            serialized_songs1={
                        'id': songs.id,
                        'title': songs.title,
                        'artist': songs.artist,
                        'duration': songs.duration,
                        'genre': songs.genre,
                        'album': songs.album.name if songs.album else "No Album",
                        'lyrics': songs.lyrics,
                        'songfile': songs.file,
                        'play_count': songs.play_count
                }
            serialized_songs.append(serialized_songs1)

        creator_albums = Album.query.filter_by(user_id=creator.id).all()
        serialized_albums=[]
        for album in creator_albums:
            if album.flagged:
                continue
            serialized_albums1 = {
                'id': album.id,
                'name': album.name,
                'artist': album.artist,
                'image': album.image,
                'genre': album.genre,
                'songs': [song.serialize() for song in album.songs]  
            } 
            serialized_albums.append(serialized_albums1)


        allalbums = Album.query.all()
        serialized_allalbums = []
        for album in allalbums:
            if album.flagged:
                continue
            ratings = Rating.query.filter_by(album_id=album.id).all()
            total_rating = sum(rating.value for rating in ratings)
            total_ratings = len(ratings)
            average_rating = total_rating / total_ratings if total_ratings != 0 else 0
            serialized_album = {
                'id': album.id,
                'name': album.name,
                'artist': album.artist,
                'image': album.image,
                'genre': album.genre,
                'user_id': album.user_id,
                'user': album.user.name,
                'average_rating': average_rating,  # Add average rating to serialized data
            }

            serialized_allalbums.append(serialized_album)

       

        allsongs = Song.query.all()
        serialized_allsongs = []
        for song in allsongs:
            if song.flagged:
                continue
            ratings = Rating.query.filter_by(song_id=song.id).all()
            total_rating = sum(rating.value for rating in ratings)
            average_rating = total_rating / len(ratings) if ratings else 0
            serialized_song = {
                'id': song.id,
                'title': song.title,
                'artist': song.artist,
                'duration': song.duration,
                'genre': song.genre,
                'album': song.album.name if song.album else "No Album",
                'lyrics': song.lyrics,
                'songfile': song.file,
                'average_rating': average_rating,
                'play_count': song.play_count
            }

            serialized_allsongs.append(serialized_song)

    

        return jsonify({
            'user': {
                'id': creator.id,
                'username': creator.username,
                'name': creator.name,
                'email': creator.email,
                'image' : creator.image,
                'date_created' : creator.date_created               
            },
            'playlists': serialized_playlists,
            'songs': serialized_songs,
            'albums': serialized_albums,
            'allalbum': serialized_allalbums,
            'allsongs': serialized_allsongs
        })
    else:
        return jsonify({"msg": "Access forbidden"})




#.........................................search......................................................
@views.route('/search', methods=['POST'])
@jwt_required()
def search():
    current_user_id = get_jwt_identity()
    try:
        data = request.json
        search_type = data.get('searchType')
        search_query = data.get('searchQuery')

        if not search_type or not search_query:
            return jsonify({'message': 'Search type and query are required'})

        if search_type == 'song':
             songs = Song.query.filter(Song.title.ilike(f'%{search_query}%')).all()
             serialized_allsongs = []
             for song in songs:
                 if  song.flagged:
                     continue
                
                 ratings = Rating.query.filter_by(song_id=song.id).all()
                 total_rating = sum(rating.value for rating in ratings)
                 average_rating = total_rating / len(ratings) if ratings else 0
                 serialized_song = {
                        'id': song.id,
                        'title': song.title,
                        'artist': song.artist,
                        'duration': song.duration,
                        'genre': song.genre,
                        'album': song.album.name if song.album else "No Album",
                        'lyrics': song.lyrics,
                        'songfile': song.file,
                        'average_rating': average_rating,
                        'play_count':song.play_count
                    }
                 serialized_allsongs.append(serialized_song)

             return jsonify({'results': serialized_allsongs})
        
        elif search_type == 'album':
            albums = Album.query.filter(Album.name.ilike(f'%{search_query}%')).all()
            serialized_allalbums = []
            for album in albums:
                if album.flagged:
                    continue
                ratings = Rating.query.filter_by(album_id=album.id).all()
                total_rating = sum(rating.value for rating in ratings)
                total_ratings = len(ratings)
                average_rating = total_rating / total_ratings if total_ratings != 0 else 0
                serialized_album = {
                    'id': album.id,
                    'name': album.name,
                    'artist': album.artist,
                    'image': album.image,
                    'genre': album.genre,
                    'user_id': album.user_id,
                    'user': album.user.name,
                    'average_rating': average_rating,  # Add average rating to serialized data
                }

                serialized_allalbums.append(serialized_album)
            return jsonify({'results': serialized_allalbums})
        
        elif search_type == 'artists':
            songs = Song.query.filter(Song.artist.ilike(f'%{search_query}%')).all()
            serialized_allsongs = []
            for song in songs:
                 if song.flagged:
                     continue
                
                 ratings = Rating.query.filter_by(song_id=song.id).all()
                 total_rating = sum(rating.value for rating in ratings)
                 average_rating = total_rating / len(ratings) if ratings else 0
                 serialized_song = {
                        'id': song.id,
                        'title': song.title,
                        'artist': song.artist,
                        'duration': song.duration,
                        'genre': song.genre,
                        'album': song.album.name if song.album else "No Album",
                        'lyrics': song.lyrics,
                        'songfile': song.file,
                        'average_rating': average_rating ,
                        'play_count':song.play_count
                    }
                 serialized_allsongs.append(serialized_song)

            return jsonify({'results': serialized_allsongs})
        
        elif search_type == 'genre':
            songs = Song.query.filter(Song.genre.ilike(f'%{search_query}%')).all()
            serialized_allsongs = []
            for song in songs:
                 if song.flagged:
                     continue
                
                 ratings = Rating.query.filter_by(song_id=song.id).all()
                 total_rating = sum(rating.value for rating in ratings)
                 average_rating = total_rating / len(ratings) if ratings else 0
                 serialized_song = {
                        'id': song.id,
                        'title': song.title,
                        'artist': song.artist,
                        'duration': song.duration,
                        'genre': song.genre,
                        'album': song.album.name if song.album else "No Album",
                        'lyrics': song.lyrics,
                        'songfile': song.file,
                        'average_rating': average_rating,
                        'play_count': song.play_count
                    }
                 serialized_allsongs.append(serialized_song)

            return jsonify({'results': serialized_allsongs})
        
        elif search_type == 'songrating':
            songs = Song.query.join(Rating).filter(Rating.value == search_query).all()
            serialized_allsongs = []
            for song in songs:
                 if song.flagged:
                     continue
                
                 ratings = Rating.query.filter_by(song_id=song.id).all()
                 total_rating = sum(rating.value for rating in ratings)
                 average_rating = total_rating / len(ratings) if ratings else 0
                 serialized_song = {
                        'id': song.id,
                        'title': song.title,
                        'artist': song.artist,
                        'duration': song.duration,
                        'genre': song.genre,
                        'album': song.album.name if song.album else "No Album",
                        'lyrics': song.lyrics,
                        'songfile': song.file,
                        'average_rating': average_rating ,
                        'play_count':song.play_count
                    }
                 serialized_allsongs.append(serialized_song)

            return jsonify({'results': serialized_allsongs})

        
        elif search_type == 'albumrating':
            albums = Album.query.join(Rating).filter(Rating.value == search_query).all()
            serialized_allalbums = []
            for album in albums:
                if album.flagged:
                    continue
                ratings = Rating.query.filter_by(album_id=album.id).all()
                total_rating = sum(rating.value for rating in ratings)
                total_ratings = len(ratings)
                average_rating = total_rating / total_ratings if total_ratings != 0 else 0
                serialized_album = {
                    'id': album.id,
                    'name': album.name,
                    'artist': album.artist,
                    'image': album.image,
                    'genre': album.genre,
                    'user_id': album.user_id,
                    'user': album.user.name,
                    'average_rating': average_rating,  # Add average rating to serialized data
                }

                serialized_allalbums.append(serialized_album)
            return jsonify({'results': serialized_allalbums})
        else:
            return jsonify({'message': 'Invalid search type'})
    except Exception as e:
        return jsonify({'message': 'Failed to perform search', 'error': str(e)})
