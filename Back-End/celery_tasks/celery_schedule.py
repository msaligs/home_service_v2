from flask import current_app as app
from celery.schedules import crontab
from celery_tasks.tasks import send_daily_service_request_emails, send_monthly_service_request_emails


celery_app = app.extensions["celery"]

@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):

    sender.add_periodic_task(
        crontab(hour=14, minute=40),  
        send_daily_service_request_emails.s(),
        name="Daily service request emails"
    )

    sender.add_periodic_task(
    crontab(day_of_month=30, hour=15, minute=49),  
    send_monthly_service_request_emails.s(),
    name="Monthly service request emails"
)

