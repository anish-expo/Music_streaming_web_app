#music v2/backend/main.py




# from tasks import *
# app = create_app()
# with app.app_context():
#  for rule in app.url_map.iter_rules():
#         print(rule)

# from Mysite.model import  Album, album_song
# app=create_app()
# with app.app_context():
#    album_id = 1
#    album = Album.query.get(album_id)
#    if album:
#       album_song_count = db.session.query(album_song).filter_by(album_id=album_id).count()
#       print(f"Number of rows in album_song table associated with album {album_id}: {album_song_count}")
#    else:
#       print("Album not found")

from application import create_app
from worker  import celery_init_app
from tasks import daily_reminder,monthly_report
from celery.schedules import crontab



app = create_app()
celery_app = celery_init_app(app)

# @celery_app.on_after_configure.connect
@celery_app.on_after_finalize.connect
def send_email(sender, **kwargs):
        sender.add_periodic_task(
            crontab(hour=11, minute=44),
            daily_reminder,
        )

@celery_app.on_after_finalize.connect
def send_report_email(sender, **kwargs):
        sender.add_periodic_task(
            crontab(hour=11, minute=39, day_of_month=22),
            monthly_report,
        )





if __name__=="__main__":
   app.run(debug=True)