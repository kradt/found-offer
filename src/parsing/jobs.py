import math
from requests_html import HTMLSession, HTML, Element
from typing import Self, Callable
from models import TypeEmploymentJobsUA, OfferModel


class PageQuery(HTML):
	def __init__(
			self, 
			session: HTMLSession,
			html: str,
			url: str,
			per_page: int,
			count_of_pages: int,
			next_page_pattern: str,
			raw_offer_classname:str,
			prepare_offer: Callable,
			current_page: int = 1):

		super().__init__(session=session, html=html, url=url)
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
			super().__init__(session=self.session, url=url, html=page_content)
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
		raw_offers: list = self.find(self.raw_offer_classname)

		while len(raw_offers) < per_page:
			self.get_next_page()
			raw_offers.append(self.find(self.raw_offer_classname))

		for i in reversed(range(0, per_page)):
			offer = raw_offers.pop(i)
			offers.append(self.prepare_offer(offer))
		return offers


class JobsUA:
	__per_page = 20
	__url = "https://jobs.ua/{}"
	__next_page = "/page-{}"
	__offer_classname = ".b-vacancy__item"

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
		return self.__url.format(filter_block)

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

	def get_count_of_pages(self, html) -> int:
		"""
		 Метод який повертає кількість сторінок в пагінації
		"""
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
		page_content = self.session.get(url)
		count_of_pages = self.get_count_of_pages(page_content.html)
		return PageQuery(
				session=self.session,
				html=page_content.content,
				count_of_pages=count_of_pages, 
				url=url, 
				per_page=self.__per_page,
				next_page_pattern=self.__next_page,
				raw_offer_classname=self.__offer_classname,
				prepare_offer=self._prepare_offer)

jobs = JobsUA()

job = "бухгалтер"
city = "kiev"
page = jobs.get_page(city=city, job=job, salary_from=1000, salary_to=70000)
vacansy = page.paginate(3, 5)
print(vacansy)

		



