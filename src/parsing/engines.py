import math
from enum import Enum
from requests_html import HTMLSession, HTML, Element
from typing import Self, Callable
from models import (TypeEmploymentJobsUA,TypeEmploymentWorkUA,
	WorkCategory, SalaryRange, SalaryWorkUA, OfferModel)


class WorkUA:
	__url = "https://www.work.ua/{}"
	__per_page = 14
	__next_page = "&page={}"
	__offer_classname = ".card-visited"

	def __init__(self):
		self.session = HTMLSession()

	def _create_link_by_filters(
			self,
			city: str | None = None,
			job: str | None = None,
			type_of_employ: tuple[TypeEmploymentWorkUA] | None = None,
			category: tuple[WorkCategory] | None = None,
			salary: SalaryRange | None = None) -> str:
		"""
		Метод який створює ссилку по потрібним фільтрам 
		"""
		link = self.__url
		filter_block = "jobs"
		filter_block += f"-{city}" if city else ""
		filter_block += f"-{job}/" if job else ""
		# Означає що будуть використувавтися розширені фільтри
		filter_block += "?advs=1"
		# Вибір категорії праці
		filter_block += f"&category={self.sum_args(category)}" if category else ""
		# Вибір виду зайнятості
		filter_block += f"&employment={self.sum_args(type_of_employ)}" if type_of_employ else ""
		# Вибір діапазону заробітньої плати
		filter_block += f"&salaryfrom={salary.FROM.value}" if salary and salary.FROM else ""
		filter_block += f"&salaryto={salary.TO.value}" if salary and salary.TO else ""
		return link.format(filter_block)

	def __get_city_of_offer(self, raw_offer) -> str:
		possible_paths = (
			'div.add-top-xs > span:nth-child(6)',
			'div.add-top-xs > span:nth-child(5)',
			'div.add-top-xs > span:nth-child(4)',
			'div.add-top-xs > span:nth-child(3)'
		)
		city = None
		for i in possible_paths:
			variant = raw_offer.find(i, first=True)
			if variant and not variant.attrs:
				city = variant
				break
		return city

	def _prepare_offer(self, raw_offer: Element) -> OfferModel:
		"""
		Метод який витягує потрібні дані з необробленого блока вакансії
		"""
		# Отримуємо блок з Заголовком в якому міститься також і ссилка
		block_title = raw_offer.find("h2")[0]
		title = block_title.text
		link = "/".join(self.__url.split("/")[0:3]) + block_title.find("a", first=True).attrs.get("href")
		# Отримуємо всі блоки обернені в тег <b> - перший з них буде зп, а другий компанією
		about_block = raw_offer.find("b")
		salary = about_block[0].text
		company = about_block[1].text if len(about_block) > 1 else ""
		# Отримуємо опис вакансії
		desc = raw_offer.find("p", first=True).text if raw_offer.find("p") else ""
		# Отримуємо місто на яке розрахована ця ваканція
		city = self.__get_city_of_offer(raw_offer)
		# Отримуємо дату публікації
		time_publish = raw_offer.find('div.col-sm-push-7.col-sm-5.col-xs-12.add-top > div > span', first=True).text
		
		return OfferModel(
			title=title, city=city.text if city else None, salary=salary, company=company, 
			description=desc, link=link, time_publish=time_publish
			)

	def _get_count_of_pages(self, html) -> int:
		"""
		 Метод який повертає кількість сторінок в пагінації
		"""
		pagination_block = html.find(".pagination", first=True)

		count_of_pages = 1
		if pagination_block:
			count_of_pages = pagination_block.find("a")[-2].text
		return int(count_of_pages)

	@staticmethod
	def sum_args(args: Enum):
		return "+".join((str(i.value) for i in args))

	def get_page(
			self,
			city: str | None = None,
			job: str | None = None, 
			type_of_employ: tuple[TypeEmploymentWorkUA] | None = None, 
			category: tuple[WorkCategory] | None = None, 
			salary: SalaryRange | None = None) -> list[OfferModel]:

		url = self._create_link_by_filters(city, job, type_of_employ, category, salary)
		page_content = self.session.get(url).html
		count_of_pages = self._get_count_of_pages(page_content)
		return PageQuery(
				session=self.session,
				html=page_content,
				count_of_pages=count_of_pages, 
				url=url, 
				per_page=self.__per_page,
				next_page_pattern=self.__next_page,
				raw_offer_classname=self.__offer_classname,
				prepare_offer=self._prepare_offer)


class JobsUA:
	url = "https://jobs.ua/{}"
	per_page = 20
	next_page_pattern = "/page-{}"
	offer_classname = ".b-vacancy__item"

	def __init__(self):
		self.session = HTMLSession()

	def _create_link_by_filters(
			self,
			city: str | None = None,
			job: str | None = None,
			type_of_employ: tuple[TypeEmploymentJobsUA] | None = None,
			salary_from: int | None = None,
			salary_to: int | None = None ) -> str:
		"""
		Метод який створює ссилку по потрібним фільтрам 
		"""
		filter_block = "vacancy/"
		filter_block += f"{city}/" if city  else ""
		filter_block += f"rabota-{job}/" if job else ""
		 # and if city in dataclass with cities
		filter_block += f"?salary={salary_from}%2C{salary_to}" if salary_from and salary_to else ""# and if salary in range
		return self.url.format(filter_block)

	def _prepare_offer(self, raw_offer: Element) -> OfferModel:
		"""
		Метод який витягує потрібні дані з необробленого блока вакансії
		"""
		# Отримуємо блок з Заголовком в якому міститься також і ссилка
		block_title = raw_offer.find(".b-vacancy__top__title")[0]
		title = block_title.text
		link = block_title.find("a", first=True).attrs.get("href")
		# Отримуємо всі блоки обернені в тег <b> - перший з них буде зп, а другий компанією
		
		salary = raw_offer.find(".b-vacancy__top__pay", first=True).text
		company = raw_offer.find("div.b-vacancy__tech > span:nth-child(1) > span", first=True).text
		# Отримуємо опис вакансії
		desc = raw_offer.find(".grey-light", first=True).text if raw_offer.find(".grey-light") else ""
		# Отримуємо місто на яке розрахована ця ваканція
		city = raw_offer.find("div.b-vacancy__tech > span:nth-child(2) > a", first=True).text
		
		return OfferModel(
			title=title, city=city if city else None, salary=salary, company=company, 
			description=desc, link=link
			)

	def _get_count_of_pages(self, url) -> int:
		"""
		 Метод який повертає кількість сторінок в пагінації
		"""
		html = self.session.get(url).html
		pagination_block = html.find(".b-vacancy__pages-title", first=True)

		count_of_pages = 1
		if pagination_block:
			count_of_pages = pagination_block.find("b:nth-child(2)", first=True).text
		return int(count_of_pages)

	def get_page(
			self,
			city: str | None = None,
			job: str | None = None, 
			type_of_employ: tuple[TypeEmploymentJobsUA] | None = None, 
			salary_from: int | None = None,
			salary_to: int | None = None ) -> list[OfferModel]:

		url = self._create_link_by_filters(city, job, type_of_employ, salary_from, salary_to)
		page_content = self.session.get(url).html
		count_of_pages = self._get_count_of_pages(page_content)
		return PageQuery(
				session=self.session,
				html=page_content,
				count_of_pages=count_of_pages, 
				url=url, 
				per_page=self.__per_page,
				next_page_pattern=self.__next_page,
				raw_offer_classname=self.__offer_classname,
				prepare_offer=self._prepare_offer)



class Query:
	def __init__(
			self,
			city: str | None = None,
			job: str | None = None,
			type_of_employ: tuple[TypeEmploymentJobsUA] | None = None,
			salary_from: int | None = None,
			salary_to: int | None = None ):

		self.job = job
		self.city = city
		self.type_of_employ = type_of_employ
		self.salary = salary_from
		self.salary_to = salary_to

	def urls(self, engines):
		return tuple(i._create_link_by_filters(
						self.city,
						self.job,
						self.type_of_employ, 
						self.salary, 
						self.salary_to) for i in engines)


class Page:
	def __init__(
			self,
			engines:list,
			query: Query,
			current_page: int = 1):

		self.engines = engines
		self.query = query
		self.urls = query.urls(self.engines)
		self.html = self.update_page()
		self.current_page = current_page


	def get_page_data(self, engines, page: int = 1) -> Self:
		"""
		Метод який змінює контент класу на контент з передної сторінки якщо вона існує
		"""
		htmls = []
		for i in engines:
			if page <= i._get_count_of_pages(self.urls[engines.index(i)]):
				url = self.urls[engines.index(i)] + i.next_page_pattern.format(page)
				page_content = i.session.get(url).content
				htmls.append(page_content)
			else:
				raise ValueError("Page don't exist")
		return htmls

	def get_next_page(self) -> Self:
		"""
		Метод який змінює контент класу на контент з наступної сторінки сайту
		"""
		next_page = self.current_page + 1
		return self.get_page(next_page)

	def update_page(self, page: int = 1) -> Self:
		"""
		Метод який змінює контент класу на контент з передної сторінки якщо вона існує
		"""
		self.current_page = page
		self.html = self.get_page_data(self.engines)

	def _get_number_needed_page(self, per_page: int, page: int) -> int:
		"""
		Метод який рахує на якій сторінці буде знаходитись потрібний діапазанон вакансій
		"""
		engines_per_page = sum(i.per_page for i in self.engines)
		return math.ceil((page * per_page) / engines_per_page)

	# Подумать
	def prepare_raw_offers(self):
		offers = []
		for engine in self.engines:
			html = self.html[self.engines.index(engine)]
			offers += [engine.prepare_html(offer) for offer in html.find(engine.raw_offer_classname)]
		return offers


	def paginate(self, per_page: int, page: int) -> list[OfferModel]:
		"""
		Метод який повертає вакансії приймаючи аргументом кількість вакансій на сторінці та номер сторінки
		"""
		offers: list[OfferModel] = []

		needed_page = self._get_number_needed_page(per_page, page)
		self.update_page(needed_page)

		raw_offers = self.prepare_raw_offers()

		for i in self.engines:
			html = self.html[self.engines.index(i)]
			raw_offers += html.find(i.raw_offer_classname)

		while len(raw_offers) < per_page:
			self.get_next_page()
			raw_offers += self.prepare_raw_offers()

		return offers


class PageQuery:
	def __init__(
			self,
			engines:list,
			session: HTMLSession,
			html: str,
			url: str,
			per_page: int,
			count_of_pages: int,
			next_page_pattern: str,
			raw_offer_classname:str,
			prepare_offer: Callable,
			current_page: int = 1):

		self.html = html
		self.session = session
		self.url = url 
		self.__per_page = per_page
		self.count_of_pages = count_of_pages
		self.current_page = current_page
		self.next_page_pattern = next_page_pattern
		self.raw_offer_classname = raw_offer_classname
		self.prepare_offer = prepare_offer

	def get_next_page(self) -> Self:
		"""
		Метод який змінює контент класу на контент з наступної сторінки сайту
		"""
		next_page = self.current_page + 1
		return self.get_page(next_page)

	def get_page(self, page: int) -> Self:
		"""
		Метод який змінює контент класу на контент з передної сторінки якщо вона існує
		"""
		if page == self.current_page:
			return self

		if page <= self.count_of_pages:
			url = self.url + self.next_page_pattern.format(page)
			page_content = self.session.get(url).content
			self.url = url
			self.html = page_content
			self.current_page = page
			return self
		else:
			raise ValueError("Page don't exist")

	def _get_number_needed_page(self, per_page: int, page: int) -> int:
		"""
		Метод який рахує на якій сторінці буде знаходитись потрібний діапазанон вакансій
		"""
		return math.ceil((page * per_page) / self.__per_page)

	def paginate(self, per_page: int, page: int) -> list[OfferModel]:
		"""
		Метод який повертає вакансії приймаючи аргументом кількість вакансій на сторінці та номер сторінки
		"""
		offers: list[OfferModel] = []

		needed_page = self._get_number_needed_page(per_page, page)
		self.get_page(needed_page)

		# block with vacancy
		raw_offers: list = self.html.find(self.raw_offer_classname)

		while len(raw_offers) < per_page:
			self.get_next_page()
			raw_offers.append(self.html.find(self.raw_offer_classname))

		for i in reversed(range(0, per_page)):
			offer = raw_offers.pop(i)
			offers.append(self.prepare_offer(offer).dict())
		return offers


jobs = JobsUA()

job = "бухгалтер"
city = "kiev"
query = Query(city=city, job=job, salary_from=1000, salary_to=70000)

page = Page([jobs], query)

print(page.paginate(1,2))

