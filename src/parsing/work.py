from requests_html import HTMLSession
from pydantic import BaseModel
from enum import Enum
from typing import Collection


class TypeEmployment(Enum):
	"""
		Перелічування видів зайнятості
		Ці дані використовуються сайтом work.ua при формуванні посилання з фільтрами які ввів користувач
		FUll = Повний Робочий день
		NOTFULL = Неповний робочий день
	"""
	FULL = 74
	NOTFULL = 75


class Salary(Enum):
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
	FROM: Salary | None
	TO: Salary | None


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


class WorkUA:
	__link = "https://www.work.ua/{}"

	def __init__(self):
		self.session = HTMLSession()


	def _create_link_by_filters(self,
								city: str | None = None,
								job: str | None = None, 
								type_of_employ: tuple[TypeEmployment] | None = None, 
								category: tuple[WorkCategory] | None = None, 
								salary: SalaryRange | None = None) -> str:
		"""
		Метод який створює ссилку по потрібним фільтрам 

		"""
		link = self.__link
		filter_block = "jobs"
		if city:
			filter_block += f"-{city}"
		if job:
			filter_block += f"-{job}/"

		# Означає що будуть використувавтися розширені фільтри
		filter_block += "?advs=1"

		# Вибір категорії праці
		if category:
			category_block = "+".join((str(i.value) for i in category))
			filter_block += f"&category={category_block}"

		# Вибір виду зайнятості
		if type_of_employ:
			type_block = "+".join((str(i.value) for i in type_of_employ))
			filter_block += f"&employment={type_block}"

		# Вибір діапазону заробітньої плати
		if salary:
			salary_block = ""
			if salary.FROM:
				salary_block += f"&salaryfrom={salary.FROM.value}"
			if salary.TO:
				salary_block += f"&salaryto={salary.TO.value}"
			filter_block += salary_block

		return link.format(filter_block)


work = WorkUA()
type_of_employ = (TypeEmployment.FULL, TypeEmployment.NOTFULL)

salary = SalaryRange(FROM=Salary.TEN, TO=Salary.THIRTY)
category = (WorkCategory.it, WorkCategory.design_art)

link = work._create_link_by_filters(city="kyiv", type_of_employ=type_of_employ, salary=salary, category=category)
print(link)
