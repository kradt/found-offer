from flask import render_template
from celery import shared_task

from src.utils import make_message
from src import mail


# Task for send message with confirm link
@shared_task()
def send_message_to_email_for_confirm_him(send_data: dict, confirm_link):
	msg = make_message("HELLO DEAR USER!", send_data)
	msg.html = render_template("confirm_email.html", confirm_link=confirm_link)
	mail.send(msg)


# Task for send code to email for reset password
@shared_task()
def send_code_to_email_for_reset_password(send_data: dict, code):
	msg = make_message("RECOVER PASSWORD", send_data)
	msg.body = f"Your code is {code}"
	mail.send(msg)
