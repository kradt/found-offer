from pydantic import BaseModel
from enum import Enum


class TypeEmploymentWorkUA(Enum):
	"""
		Перелічування видів зайнятості
		Ці дані використовуються сайтом work.ua при формуванні посилання з фільтрами які ввів користувач
		FUll = Повний Робочий день
		NOTFULL = Неповний робочий день
	"""
	FULL = 74
	NOTFULL = 75


class TypeEmploymentJobsUA(Enum):
	FULL = 1
	NOTFULL = 5


class SalaryWorkUA(Enum):
	"""
		Перелічування тисяч гривень
		Ці дані використовуються сайтом work.ua при формуванні посилання з фільтрами які ввів користувач
	"""
	ANY = 0
	THREE = 2
	FIVE = 3
	SEVEN = 4
	TEN = 5
	FIFTEEN = 6
	TWENTY = 7
	THIRTY = 8
	FIFTY = 9


class SalaryRange(BaseModel):
	"""
		Структура данних для формування діапазону заробітньої плати необхідної користувачеві.
	"""
	FROM: SalaryWorkUA | None
	TO: SalaryWorkUA | None


class WorkCategory(Enum):
	"""
		Перелічування всіх можливих категорій роботи
		Ці дані використовуються сайтом work.ua при формуванні посилання з фільтрами які ввів користувач
	"""
	customer_service = 20
	production_engineering = 14
	sales = 22
	retail = 23 
	jobs_administration = 2
	logistic_supply_chain = 8
	hotel_restaurant_tourism = 4
	it = 1
	accounting = 3
	auto_transport = 24
	healthcare = 10
	marketing_advertising_pr = 9
	office_secretarial = 15
	banking_finance = 26
	telecommunications = 6792
	construction_architecture = 19
	education_scientific = 12
	beauty_sports = 6
	design_art = 5
	publishing_media = 17
	hr_recruitment = 25
	security = 13
	management_executive = 21
	agriculture = 30
	legal = 27
	real_estate = 11
	culture_music_showbiz = 7
	insurance = 18


class OfferModel(BaseModel):
	"""
	Модель Вакансії
	"""
	title: str
	city: str | None
	salary: str | None
	company: str
	description: str
	link: str
	time_publish: str | None