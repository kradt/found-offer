import re
import datetime
from requests_html import Element

from ..models import OfferModel
from .abc import PageQuery


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
