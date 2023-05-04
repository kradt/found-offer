from celery import shared_task
from flask import render_template
from flask_mail import Message

from src import mail


def make_message(message, send_data):
	msg = Message(
		message,
		sender=send_data["sender"],
		recipients=send_data["recipients"])
	return msg


@shared_task
def send_message_to_email_for_confirm_him(send_data: dict, confirm_link):
	msg = make_message("HELLO DEAR USER!", send_data)
	msg.html = render_template("confirm_email.html", confirm_link=confirm_link)
	mail.send(msg)


@shared_task
def send_code_to_email_for_reset_password(send_data: dict, code):
	msg = make_message("RECOVER PASSWORD", send_data)
	msg.body = f"Your code is {code}"
	mail.send(msg)
