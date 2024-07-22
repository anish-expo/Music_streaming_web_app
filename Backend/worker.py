#Backend/Mysite/worker.py

# from celery import Celery, Task

# def celery_init_app(app):
#     class FlaskTask(Task):
#         def __call__(self, *args: object, **kwargs: object) -> object:
#             with app.app_context():
#                 return self.run(*args, **kwargs)

#     celery_app = Celery(app.name, task_cls=FlaskTask)
#     celery_app.config_from_object("celeryconfig")
#     return celery_app

from celery import Celery, Task
from flask import current_app
from application import create_app
app1=create_app()

class FlaskTask(Task):
    def __call__(self, *args: object, **kwargs: object) -> object:
        with app1.app_context():
            return self.run(*args, **kwargs)

def celery_init_app(app):
    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object("celeryconfig")
    return celery_app