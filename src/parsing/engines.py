import re
import datetime
from requests_html import HTMLSession, Element

from .models import OfferModel


class PageQuery:
	"""
		Interface for realize iterator pattern
	"""
	_url = ...
	_offer_classname = ...
	_offers_pattern = ...
	_next_page_pattern = ...

	def __init__(self, current_page: int = 1) -> None:
		self.session = HTMLSession()
		self.current_page = current_page
		self.count_of_pages = self._get_count_of_pages()

	def _is_offer_element(self, elem: Element) -> bool:
		pass

	def _prepare_offer(self, raw_offer: Element) -> OfferModel:
		pass

	def _get_count_of_pages(self) -> int:
		pass

	def _make_list_of_offers(self, raw_offers: list) -> list:
		offers_in_page: list = []
		for offer in raw_offers:
			if self._is_offer_element(offer):
				offers_in_page.append(self._prepare_offer(offer))

		return offers_in_page

	def set_default(self):
		self.__init__()

	def __iter__(self):
		return self

	def __next__(self) -> list:
		self.current_page += 1
		necessary_url = self._url.format(self._offers_pattern + self._next_page_pattern.format(self.current_page))
		if self.current_page > self.count_of_pages:
			raise StopIteration("End of pages")

		page_html = self.session.get(necessary_url).html
		raw_offers = page_html.find(self._offer_classname)
		return self._make_list_of_offers(raw_offers)


class WorkUA(PageQuery):
	"""
		Class realize parser WorkUA
	"""
	_url = "https://www.work.ua/{}"
	_offers_pattern = "jobs/?ss=1"
	_per_page = 14
	_next_page_pattern = "&page={}"
	_offer_classname = ".card-visited"

	def __init__(self, current_page: int = 0) -> None:
		super().__init__(current_page)
		self.count_of_pages = self._get_count_of_pages()

	@staticmethod
	def __get_city_of_offer(raw_offer: Element) -> str | None:
		possible_paths = (
			'div.add-top-xs > span:nth-child(8)',
			'div.add-top-xs > span:nth-child(7)',
			'div.add-top-xs > span:nth-child(6)',
			'div.add-top-xs > span:nth-child(5)',
			'div.add-top-xs > span:nth-child(4)',
			'div.add-top-xs > span:nth-child(3)'
		)
		city = None
		for path in possible_paths:
			variant = raw_offer.find(path, first=True)
			if variant and not variant.attrs:
				city = variant
				break
		return city

	def _is_offer_element(self, elem: Element) -> bool:
		return True

	@staticmethod
	def __get_time_from_str(time_str: str) -> datetime.datetime:
		necessary_time = datetime.datetime.now()
		if time_str == "вчора":
			return necessary_time - datetime.timedelta(days=1)
		elif time_str == "Гаряча":
			return necessary_time

		before_publish_time = time_str.split()
		digit = int(before_publish_time[0])
		time_marker = before_publish_time[1]

		if time_marker == "хв.":
			necessary_time -= datetime.timedelta(minutes=digit)
		elif time_marker == "год.":
			necessary_time -= datetime.timedelta(hours=digit)
		elif time_marker == "дні.":
			necessary_time -= datetime.timedelta(days=digit)
		elif time_marker == "тиж.":
			necessary_time -= datetime.timedelta(weeks=digit)
		elif time_marker == "міс.":
			necessary_time -= datetime.timedelta(weeks=digit * 4)
		return necessary_time

	def _prepare_offer(self, raw_offer: Element) -> OfferModel:
		"""
		Метод який витягує потрібні дані з необробленого блока вакансії
		"""
		# Отримуємо блок з Заголовком в якому міститься також і ссилка
		block_title = raw_offer.find("h2")[0]
		title = block_title.text
		link = "/".join(self._url.split("/")[0:3]) + block_title.find("a", first=True).attrs.get("href")
		# Отримуємо всі блоки обернені в тег <b> - перший з них буде зп, а другий компанією
		about_block = raw_offer.find("b")

		# Make better realize of extract salary
		salary = about_block[0].text
		extracted_salary = re.findall(r'\d+', ''.join(salary.split()))
		salary_to = float(extracted_salary.pop()) if extracted_salary else None
		salary_from = float(extracted_salary.pop()) if extracted_salary else None
		salary_from = salary_to if salary_to and not salary_from else salary_from
		company = raw_offer.find(".add-top-xs > span:nth-child(1)", first=True).text
		# Отримуємо опис вакансії
		desc = raw_offer.find("p", first=True).text if raw_offer.find("p") else ""
		# Отримуємо місто на яке розрахована ця ваканція
		city = self.__get_city_of_offer(raw_offer)
		# Отримуємо дату публікації
		time_publish_data = raw_offer.find('div.pull-right.no-pull-xs.nowrap > span.text-muted.small', first=True) or \
							raw_offer.find("div.pull-right.no-pull-xs.nowrap > span.label.label-orange-light", first=True)
		time_publish = self.__get_time_from_str(time_publish_data.text)

		return OfferModel(
			title=title, city=city.text if city else None, salary_from=salary_from, salary_to=salary_to,
			company=company, description=desc, link=link, time_publish=time_publish or None
		)

	def _get_count_of_pages(self) -> int:
		"""
		Метод який повертає кількість сторінок в пагінації
		"""
		url = self._url.format(self._offers_pattern)
		html = self.session.get(url).html
		pagination_block = html.find(".pagination", first=True)

		count_of_pages = 1
		if pagination_block:
			count_of_pages = pagination_block.find("a")[-2].text
		return int(count_of_pages)


class JobsUA(PageQuery):
	"""
		Class realize parser JobsUA
	"""
	_url = "https://jobs.ua/{}"
	_per_page = 20
	_next_page_pattern = "/page-{}"
	_offers_pattern = "vacancy"
	_offer_classname = ".b-vacancy__item.js-item_list"

	def __init__(self, current_page: int = 0) -> None:
		super().__init__(current_page)
		self.month_to_number_dict = {
			"січня": 1,
			"лютого": 2,
			"березня": 3,
			"квітня": 4,
			"травня": 5,
			"червня": 6,
			"липня": 7,
			"серпня": 8,
			"вересня": 9,
			"жовтня": 10,
			"листопада": 11,
			"грудня": 12
		}
		self.count_of_pages = self._get_count_of_pages()

	def _is_offer_element(self, elem: Element) -> bool:
		return elem.attrs.get("id") if elem.attrs else False

	def __extract_date(self, link: str) -> datetime.datetime:
		necessary_date = datetime.datetime.now()

		data = self.session.get(link).html
		link = data.find("div.b-vacancy-full__tech-wrapper > span.b-vacancy-full__tech__item.m-r-1", first=True).text
		items = link.split()
		month = items[1]
		day = items[0]
		try:
			year = items[2]
		except IndexError:
			year = necessary_date.year

		return necessary_date.replace(
			year=int(year),
			month=self.month_to_number_dict[month],
			day=int(day))

	def _prepare_offer(self, raw_offer: Element) -> OfferModel:
		"""
		Метод який витягує потрібні дані з необробленого блока вакансії
		"""
		# Отримуємо блок з Заголовком в якому міститься також і ссилка
		block_title = raw_offer.find("a.b-vacancy__top__title", first=True)
		title = str(block_title.text) if block_title else ""
		link = block_title.attrs.get("href")

		salary = raw_offer.find(".b-vacancy__top__pay", first=True)
		salary = salary.text if salary else ""
		extracted_salary = re.findall(r'\d+', ''.join(salary.split()))
		salary_from = float(extracted_salary.pop()) if extracted_salary else None
		salary_to = salary_from

		company = str(raw_offer.find("div.b-vacancy__tech > span:nth-child(1) > span", first=True).text)
		# Отримуємо опис вакансії
		desc = raw_offer.find(".grey-light", first=True)
		desc = str(desc.text) if desc else ""
		# Отримуємо місто на яке розрахована ця ваканція
		city = str(raw_offer.find("div.b-vacancy__tech > span:nth-child(2) > a", first=True).text)
		time_publish = self.__extract_date(link)
		return OfferModel(
			title=title, city=city if city else None, salary_from=salary_from, salary_to=salary_to, company=company,
			description=desc, link=link, time_publish=time_publish
		)

	def _get_count_of_pages(self) -> int:
		"""
		Метод який повертає кількість сторінок в пагінації
		"""
		url = self._url.format(self._offers_pattern)
		html = self.session.get(url).html
		count_of_pages = html.find(".b-vacancy__pages-title > span:nth-child(1) > b:nth-child(2)", first=True)
		count_of_pages = int(count_of_pages.text) if count_of_pages else 1
		return count_of_pages
