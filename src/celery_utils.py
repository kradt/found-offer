import datetime

from flask import Flask
from celery import Celery, Task


def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.conf.beat_schedule = {
        "parse_to_base_work_ua": {
            "task": "src.root.tasks.parse_work_ua_to_base",
            "schedule": datetime.timedelta(hours=24)
        },
        "parse_to_base_jobs_ua": {
            "task": "src.root.tasks.parse_jobs_ua_to_base",
            "schedule": datetime.timedelta(hours=24)
        },
        "remove_old_vacancies": {
            "task": "src.root.tasks.remove_old_vacancies",
            "schedule": datetime.timedelta(hours=24)
        },
        "find_user_vacancies": {
            "task": "src.root.tasks.find_user_vacancies",
            "schedule": datetime.timedelta(minutes=1)
        }
    }
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app
