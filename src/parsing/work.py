from requests_html import HTMLSession, HTML, Element, BaseParser
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


class OfferModel(BaseModel):
	"""
	Модель Вакансії
	"""
	title: str
	city: str
	salary: str | None
	company: str
	description: str
	link: str


class PageQuery(HTML):
	"""
	Клас який представляє запит вакансій по фільтрам
	"""
	def __init__(self, *args, per_page: int, current_page: int = 1, **kwargs):
		super().__init__(*args, **kwargs)
		self.count_of_pages = self.get_count_of_pages()
		self._current_page = current_page
		self.__per_page = per_page


	def get_offers(self) -> list[OfferModel]:
		offers: list[OfferModel] = []

		raw_offers: list = self.find(".card-visited")

		for offer in raw_offers:
			# Отримуємо блок з Заголовком в якому міститься також і ссилка
			block_title = offer.find("h2")[0]
			title = block_title.text
			link = "/".join(self.url.split("/")[0:3]) + block_title.find("a", first=True).attrs["href"]
			# Отримуємо всі блоки обернені в тег <b> - перший з них буде зп, а другий компанією
			about_block = offer.find("b")
			salary = about_block[0].text
			company = about_block[1].text
			# Отримуємо опис вакансії
			desc = offer.find("p")[0].text
			# Отримуємо місто на яке розрахована ця ваканція
			city = offer.find('div.add-top-xs > span:nth-child(6)', first=True)
			# ---- TODO: Зробить по людьські ----
			if not city or city.attrs:
				city = offer.find('div.add-top-xs > span:nth-child(4)', first=True)
				if not city or city.attrs:
					city = offer.find('div.add-top-xs > span:nth-child(5)', first=True)
				if not city or city.attrs:
					city = offer.find('div.add-top-xs > span:nth-child(3)', first=True)
			
			offers.append(OfferModel(title=title,
							  		 city=city.text, 
							  		 salary=salary, 
							  		 company=company, 
							 		 description=desc,
							 	 	 link=link))
		return offers

	def get_count_of_pages(self) -> int:
		"""
		 Метод який повертає кількість сторінок в пагінації
		"""
		pagination_block = self.find(".pagination", first=True)

		count_of_pages = 1
		if pagination_block:
			count_of_pages = pagination_block.find("a")[-2].text
		return int(count_of_pages)

	@property
	def current_page(self) -> int:
		return self._current_page

	@current_page.setter
	def current_page(self, value: int):
		if isinstance(value, int) and value <= self.count_of_pages:
			html = self.session.get(self.url + f"&page={value}").content
			# Викликаємо батьківський дандер метод __init__ для того щоб примінити новий html
			super().__init__(session=self.session, url=self.url, html=html)
			self._current_page = value
		else:
			raise ValueError(f"The Query has only {self.count_of_pages} pages")

class WorkUA:
	__url = "https://www.work.ua/{}"

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
		link = self.__url
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

	def get_page(self,
				 city: str | None = None,
				 job: str | None = None, 
				 type_of_employ: tuple[TypeEmployment] | None = None, 
				 category: tuple[WorkCategory] | None = None, 
				 salary: SalaryRange | None = None) -> list[OfferModel]:

		url = self._create_link_by_filters(city, job, type_of_employ, category, salary)
		page_content = self.session.get(url).content
		return PageQuery(session=self.session, html=page_content, url=url, per_page=28)


work = WorkUA()
type_of_employ = (TypeEmployment.FULL, TypeEmployment.NOTFULL)
salary = SalaryRange(FROM=Salary.THREE, TO=Salary.FIFTY)
pg = work.get_page(job="backend", type_of_employ=type_of_employ, salary=salary)
pg.current_page = 3

print(pg.get_offers())
print(pg.current_page)


