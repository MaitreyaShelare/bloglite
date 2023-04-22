from celery import Celery
from celery.schedules import crontab


def make_celery(app):
    celery = Celery(app.import_name)
    celery.conf.update(app.config["CELERY_CONFIG"])

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)
            
    celery.Task = ContextTask

    celery.conf.beat_schedule = {
        'daily_reminder': {
            'task': 'tasks.daily_reminder',
            'schedule': crontab(hour=20, minute=0), 
        },
        'monthly_report': {
            'task': 'tasks.monthly_report',
            'schedule': crontab(hour=10, minute=17),
            # 'schedule': crontab(day_of_month='1', hour='0', minute='0'),
    },
    }
    
    celery.conf.timezone = 'Asia/Kolkata'

    return celery
