import datetime

from flask import Flask
from celery import Celery, Task

from src.parsing import engines


def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    CELERYBEAT_SCHEDULER = {
        "start_parse_to_base": {
            "task": "src.auth.tasks.start_parse_to_base",
            "schedule": datetime.timedelta(minutes=1),
            "args": (engines.JobsUA(),)

        }
    }
    app.config["CELERYBEAT_SCHEDULER"] = CELERYBEAT_SCHEDULER
    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app
