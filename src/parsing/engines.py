import math
from enum import Enum
from requests_html import HTMLSession, HTML, Element
from typing import Self, Callable
from models import (TypeEmploymentJobsUA,TypeEmploymentWorkUA,
	WorkCategory, SalaryRange, SalaryWorkUA, OfferModel)


class WorkUA:
	url = "https://www.work.ua/{}"
	per_page = 14
	next_page_pattern = "&page={}"
	offer_classname = ".card-visited"

	def __init__(self):
		self.session = HTMLSession()

	def is_offer_element(self, elem):
		return True

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
		link = self.url
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
		link = "/".join(self.url.split("/")[0:3]) + block_title.find("a", first=True).attrs.get("href")
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

	def _get_count_of_pages(self, url) -> int:
		"""
		 Метод який повертає кількість сторінок в пагінації
		"""
		html = self.session.get(url).html
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

		query = Query(city, job, type_of_employ, salary.FROM, salary.TO)
		return PageQuery(engines=[self], query=query)


class JobsUA:
	url = "https://jobs.ua/{}"
	per_page = 20
	next_page_pattern = "/page-{}"
	offer_classname = ".b-vacancy__item.js-item_list"

	def __init__(self):
		self.session = HTMLSession()

	def is_offer_element(self, elem: Element):
		return elem.attrs.get("id") if elem.attrs else False
		
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

		block_title = raw_offer.find(".b-vacancy__top__title", first=True)
		title = block_title.text
		link = block_title.find("a", first=True).attrs.get("href")
		# Отримуємо всі блоки обернені в тег <b> - перший з них буде зп, а другий компанією
		
		salary = raw_offer.find(".b-vacancy__top__pay", first=True)
		salary = salary.text if salary else ""
		
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

		query = Query(city, job, type_of_employ, salary_from, salary_to)
		return PageQuery(engines=[self], query=query)


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


class PageQuery:
	def __init__(
			self,
			engines: list,
			query: Query,
			current_page: int = 1):

		self.engines = engines
		self.query = query
		self.urls = query.urls(self.engines)
		self.html = self._update_page()
		self.current_page = current_page


	def _get_page_data(self, engines, page: int = 1) -> Self:
		"""
		Метод який змінює контент класу на контент з передної сторінки якщо вона існує
		"""
		htmls = []
		for i in engines:
			if page <= i._get_count_of_pages(self.urls[engines.index(i)]):
				url = self.urls[engines.index(i)] + i.next_page_pattern.format(page)
				page_content = i.session.get(url).html
				htmls.append(page_content)
			else:
				raise ValueError("Page don't exist")
		return htmls

	def _get_next_page(self) -> Self:
		"""
		Метод який змінює контент класу на контент з наступної сторінки сайту
		"""
		next_page = self.current_page + 1
		return self._update_page(next_page)

	def _update_page(self, page: int = 1) -> Self:
		"""
		Метод який змінює контент класу на контент з передної сторінки якщо вона існує
		"""
		self.current_page = page
		self.html = self._get_page_data(self.engines, page)

	def _get_number_needed_page(self, per_page: int, page: int) -> int:
		"""
		Метод який рахує на якій сторінці буде знаходитись потрібний діапазанон вакансій
		"""
		engines_per_page = sum(i.per_page for i in self.engines)
		needed_page = math.ceil(((page * per_page) - per_page) / engines_per_page)
		return needed_page if needed_page > 0 else 1

	# Подумать
	def _prepare_raw_offers(self):
		offers = []
		for engine in self.engines:
			html = self.html[self.engines.index(engine)]
			offers += [engine._prepare_offer(offer) for offer in html.find(engine.offer_classname) if engine.is_offer_element(offer)]
		return offers

	def _get_shift_of_page(self, per_page, page):
		engines_per_page = sum(i.per_page for i in self.engines)
		return ((page*per_page)-per_page) - (self.current_page-1) * engines_per_page

	def paginate(self, per_page: int, page: int) -> list[OfferModel]:
		"""
		Метод який повертає вакансії приймаючи аргументом кількість вакансій на сторінці та номер сторінки
		"""
		offers: list[OfferModel] = []

		needed_page = self._get_number_needed_page(per_page, page)
		self._update_page(needed_page)

		shift = self._get_shift_of_page(per_page, page)
		offers: list[OfferModel] = self._prepare_raw_offers()[shift:]

		while len(offers) < per_page:
			self._get_next_page()
			offers += self._prepare_raw_offers()

		return offers[:per_page]

jobs = JobsUA()
work = WorkUA()


job = "бухгалтер"
city = "kiev"
query = Query(job=job)

page = PageQuery([work, jobs], query)

a = page.paginate(5, 14)
for i in a:
	print(i,end="\n\n")

