import datetime
import os
import mongoengine
from typing import Iterator
from loguru import logger

from src.parsing import engines
from src.database import models
from src.config import Config

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


@shared_task()
def send_message_to_email_for_confirm_him(send_data: dict, confirm_link):
	msg = make_message("HELLO DEAR USER!", send_data)
	msg.html = render_template("confirm_email.html", confirm_link=confirm_link)
	mail.send(msg)


@shared_task
def send_code_to_email_for_reset_password(send_data: dict, code):
	msg = make_message("RECOVER PASSWORD", send_data)
	msg.body = f"Your code is {code}"
	mail.send(msg)


def save_offers_to_base(offers: list) -> int:
	"""
	Function saving offers to base and return amount of saved offers
	"""
	added_to_base_offers = 0
	for offer in offers:
		if not models.Vacancy.objects(
				title=offer.title, city=offer.city,
				salary_from=offer.salary_from, company=offer.company):
			models.Vacancy(**offer.dict()).save()
			added_to_base_offers += 1

	return added_to_base_offers


def write_offer_to_base(offers_engine: Iterator):
	logger.debug(f"{os.getpid()} was start")
	mongoengine.connect(host=Config.MONGODB_SETTINGS["host"])

	total_sum_offers = 0
	offers_engine.by_default()
	try:
		for offers in offers_engine:
			len_saved_offers = save_offers_to_base(offers)
			total_sum_offers += len_saved_offers
			logger.debug(f"{total_sum_offers} offers from {offers_engine} were saved in base")
	except Exception as e:
		logger.exception(e)
	logger.debug(f"{total_sum_offers} offers from {offers_engine} Successfully added to base")


@shared_task
def parse_work_ua_to_base():
	parser = engines.WorkUA()
	write_offer_to_base(parser)
	logger.debug("Work UA processes were start!")


@shared_task
def parse_jobs_ua_to_base():
	parser = engines.JobsUA()
	write_offer_to_base(parser)
	logger.debug("Jobs UA processes were start!")

@shared_task
def remove_old_vacancies():
	month_ago = datetime.datetime.now()-datetime.timedelta(days=30)
	old_vacancies = models.Vacancy.objects(time_publish__lte=month_ago)
	count_of_del_vacancies = old_vacancies.count()
	old_vacancies.delete()
	logger.debug(f"{count_of_del_vacancies} vacancies were deleted ")


@shared_task
def find_user_vacancies():
	for user in models.User.objects():
		search_patterns = user.auto_search
		for search_pattern in search_patterns:
			necessary_vacancies = models.Vacancy.objects(
				title__icontains=search_pattern["title"],
				city__icontains=search_pattern["city"],
				salary_from__gte=search_pattern["salary"],
				time_publish__lte=search_pattern["start_search"])
			if necessary_vacancies:
				search_patterns[search_patterns.index(search_pattern)].time_publish = datetime.datetime.now()
				user.update(auto_search=search_patterns)
				send_data = {
					"sender": Config.MAIL_DEFAULT_SENDER,
					"recipients": [user.email],
				}
				msg = make_message("Hello dear user", send_data)
				msg.html = render_template("template_for_vacancy.html", vacancies=necessary_vacancies)
				mail.send(msg)
				logger.debug(f"vacancies sussefully send to {user.email} ")
