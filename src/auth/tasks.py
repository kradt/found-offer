from celery import shared_task
from flask import render_template
from flask_mail import Message
from src import mail


@shared_task()
def send_message_to_email(send_data: dict, confirm_link):
	msg = Message(
		"HELLO DEAR USER!",
		sender=send_data["sender"],
		recipients=send_data["recipients"])
	msg.html = render_template("confirm_email.html", confirm_link=confirm_link)
	mail.send(msg)