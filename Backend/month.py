from application.model import User,Song,Album
from datetime import datetime, timedelta
from application import create_app
app=create_app()

def daily_reminder():
    with app.app_context():
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
        return data1
print(daily_reminder())


# def monthly_report():
#     with app.app_context():
#         end_date = datetime.today()  # Get the current date without time, and set day to 1
#         start_date = end_date - timedelta(days=30)  # Subtract 30 days to get the start date
#         current_month = end_date.strftime('%B %Y')
#         print(end_date)
#         print(start_date)
#         print(current_month)

#         creators = User.query.filter_by(role_id=3).all()
#         data = []
#         for creator in creators:
#             songs_created = Song.query.filter(
#                 Song.author == creator.id,
#                 Song.date_created >= start_date,
#                 Song.date_created < end_date
#             ).count()

#             albums_created = Album.query.filter(
#                 Album.user_id == creator.id,
#                 Album.date_created >= start_date,
#                 Album.date_created < end_date
#             ).count()

#             creator_data = {
#                 'name': creator.name,
#                 'email': creator.email,
#                 'songs_created': songs_created,
#                 'albums_created': albums_created
#             }
#             data.append(creator_data)
#         return data

# print(monthly_report())
