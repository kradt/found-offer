from requests_html import HTMLSession
from pydantic import BaseModel
from enum import Enum


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



class Offer(BaseModel):
	title: str
	city: str
	salary: str | None
	company: str
	description: str
	link: str


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

	def get_count_of_pages(self, link: str) -> int:
		"""
		 Метод який повертає кількість сторінок в пагінації
		"""
		#TODO: ЗРобить щоб якщо немає сторінок повертало False
		page = self.session.get(link).html
		pagination_block = page.find(".pagination", first=True)
		count_of_pages = pagination_block.find("a")[-2].text
		return int(count_of_pages)
		
	def get_offers(self,
				   city: str | None = None,
				   job: str | None = None, 
				   type_of_employ: tuple[TypeEmployment] | None = None, 
				   category: tuple[WorkCategory] | None = None, 
				   salary: SalaryRange | None = None) -> list[Offer]:

		link = self._create_link_by_filters(city, job, type_of_employ, category, salary)
		page = self.session.get(link)
		offers: list[Offer] = []
		for i in page.html.find(".card-visited"):
			# Отримуємо блок з Заголовком в якому міститься також і ссилка
			block_title = i.find("h2")[0]
			title = block_title.text
			# Отримуємо ссилку на вакансію зрізаючи перший символ "/" оскільки в змінній __link він уже присутній
			link = self.__link.format(block_title.find("a", first=True).attrs["href"][1:-1])
			# Отримуємо всі блоки обернені в тег <b> - перший з них буде зп, а другий компанією
			about_block = i.find("b")
			salary = about_block[0].text
			company = about_block[1].text
			# Отримуємо опис вакансії
			desc = i.find("p")[0].text
			# Отримуємо місто на яке розрахована ця ваканція
			city = i.find('div.add-top-xs > span:nth-child(6)', first=True)
			#---- TODO: Зробить по людьські ----
			if not city or city.attrs:
				city = i.find('div.add-top-xs > span:nth-child(4)', first=True)

				if not city or city.attrs:
					city = i.find('div.add-top-xs > span:nth-child(5)', first=True)
				if not city or city.attrs:
					city = i.find('div.add-top-xs > span:nth-child(3)', first=True)
			#------------------------------------
	
			offers.append(Offer(title=title,
						  		city=city.text, 
						  		salary=salary, 
						  		company=company, 
						 		description=desc,
						 	 	link=link))
		return offers

work = WorkUA()
type_of_employ = (TypeEmployment.FULL, TypeEmployment.NOTFULL)
salary = SalaryRange(FROM=Salary.THREE, TO=Salary.FIFTY)
category = (WorkCategory.it,)
offers = work.get_offers(city="kyiv", type_of_employ=type_of_employ, salary=salary, category=category)

print(offers)
print(len(offers))

