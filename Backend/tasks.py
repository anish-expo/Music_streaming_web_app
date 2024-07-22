#Backend/tasks.py

from application.model import User,Song,Album
from datetime import datetime, timedelta
from flask import render_template

from mail_service import send_message
from celery import Celery
celery = Celery()
from application import create_app
app=create_app()

# @shared_task(ignore_result=True)
# @celery.task()
# def daily_reminder():
#     recent_login_threshold = datetime.now() - timedelta(days=1)
#     users = User.query.filter_by(role_id=2).all()
#     data1=[]
#     for user in users:
#         if user.last_login is None or user.last_login < recent_login_threshold:
#             user_data = {
#             'name': user.name,
#             'email': user.email,
            
#         }
#         data1.append(user_data)
#     html_content_template = render_template('reminder.html', data=data1)
#     for user_data in data1:
#         personalized_content = render_template('reminder.html', data=user_data['name'])
#         send_message(to=user_data['email'], subject=f"Remainder ", content_body=personalized_content)

@celery.task()
def daily_reminder():
    recent_login_threshold = datetime.now() - timedelta(days=1)
    users = User.query.filter_by(role_id=2).all()
    data1=[]
    for user in users:
        if user.last_login is None or user.last_login < recent_login_threshold:
            user_data = {
            'name': user.name,
            'email': user.email,
            
        }
        data1.append(user_data)
    html_content_template = render_template('user_reminder.html', data=data1)
    for user_data in data1:
        personalized_content = render_template('user_reminder.html', data=user_data['name'])
        send_message(to=user_data['email'], subject=f"Reminder ", content_body=personalized_content)



                
    

@celery.task()
def monthly_report():
    end_date = datetime.now() 
    start_date = end_date - timedelta(days=30)  
    current_month = end_date.strftime('%B %Y')

    creators = User.query.filter_by(role_id=3).all()
    data = []
    for creator in creators:
        songs_created = Song.query.filter(
            Song.author == creator.id,
            Song.date_created >= start_date,
            Song.date_created < end_date
        ).count()

        albums_created = Album.query.filter(
            Album.user_id == creator.id,
            Album.date_created >= start_date,
            Album.date_created < end_date
        ).count()

        creator_data = {
            'name': creator.name,
            'email': creator.email,
            'songs_created': songs_created,
            'albums_created': albums_created
        }
        data.append(creator_data)

    html_content_template = render_template('monthly_report.html', month=current_month, data=data)
    for creator_data in data:
        personalized_content = render_template('monthly_report.html', month=current_month, data=[creator_data])
        send_message(to=creator_data['email'], subject=f"Monthly Progress Report - {current_month}", content_body=personalized_content)

        




       
    

      
