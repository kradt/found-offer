from celery import shared_task
from flask_mail import Message
from src import mail


@shared_task()
def send_message_to_email(send_data: dict):
	msg = Message(
		"Everything will be fine",
		sender=send_data["sender"],
		recipients=send_data["recipients"])
	mail.send(msg)