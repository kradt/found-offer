from typing import Self
from requests_html import HTMLSession, HTML, Element, BaseParser
import math
from enum import Enum
from models import TypeEmployment, SalaryRange, Salary, WorkCategory, OfferModel

class PageQuery(HTML):
	"""
	Клас який представляє запит вакансій по фільтрам
	"""
	def __init__(self, *args, per_page: int, current_page: int = 1, **kwargs):
		super().__init__(*args, **kwargs)
		self.__per_page = per_page
		self.count_of_pages = self.get_count_of_pages()
		self.current_page = current_page

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
		company = about_block[1].text
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

	def get_count_of_pages(self) -> int:
		"""
		 Метод який повертає кількість сторінок в пагінації
		"""
		pagination_block = self.find(".pagination", first=True)

		count_of_pages = 1
		if pagination_block:
			count_of_pages = pagination_block.find("a")[-2].text
		return int(count_of_pages)

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
			url = self.url + f"&page={page}"
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

		raw_offers: list = self.find(".card-visited")

		while len(raw_offers) < per_page:
			self.get_next_page()
			raw_offers.append(self.find(".card-visited"))

		for i in reversed(range(0, per_page)):
			offer = raw_offers.pop(i)
			offers.append(self._prepare_offer(offer))
		return offers


class WorkUA:
	__url = "https://www.work.ua/{}"
	__per_page = 14

	def __init__(self):
		self.session = HTMLSession()

	def _create_link_by_filters(
			self,
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

	@staticmethod
	def sum_args(args: Enum):
		return "+".join((str(i.value) for i in args))

	def get_page(
			self,
			city: str | None = None,
			job: str | None = None, 
			type_of_employ: tuple[TypeEmployment] | None = None, 
			category: tuple[WorkCategory] | None = None, 
			salary: SalaryRange | None = None) -> list[OfferModel]:

		url = self._create_link_by_filters(city, job, type_of_employ, category, salary)
		page_content = self.session.get(url).content
		return PageQuery(session=self.session, html=page_content, url=url, per_page=self.__per_page)
		


work = WorkUA()
type_of_employ = (TypeEmployment.FULL, TypeEmployment.NOTFULL)
salary = SalaryRange(FROM=Salary.THREE, TO=Salary.FIFTY)
pg = work.get_page(job="backend", type_of_employ=type_of_employ, salary=salary)
print(pg.url)
print(pg.paginate(14, 1))




