import math
from requests_html import HTMLSession, Element
from slugify import slugify

from .models import OfferModel


class WorkUA:
	url = "https://www.work.ua/{}"
	per_page = 14
	next_page_pattern = "&page={}"
	offer_classname = ".card-visited"

	def __init__(self):
		self.session = HTMLSession()


	@staticmethod
	def __get_city_of_offer(raw_offer: Element) -> str | None:
		possible_paths = (
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

	def prepare_offer(self, raw_offer: Element) -> OfferModel:
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

	def get_count_of_pages(self, url) -> int:
		"""
		Метод який повертає кількість сторінок в пагінації
		"""
		html = self.session.get(url).html
		pagination_block = html.find(".pagination", first=True)

		count_of_pages = 1
		if pagination_block:
			count_of_pages = pagination_block.find("a")[-2].text
		return int(count_of_pages)



class JobsUA:
	url = "https://jobs.ua/{}"
	per_page = 20
	next_page_pattern = "/page-{}"
	offer_classname = ".b-vacancy__item.js-item_list"

	def __init__(self):
		self.session = HTMLSession()


	@staticmethod
	def prepare_offer(raw_offer: Element) -> OfferModel:
		"""
		Метод який витягує потрібні дані з необробленого блока вакансії
		"""
		# Отримуємо блок з Заголовком в якому міститься також і ссилка

		block_title = raw_offer.find("a.b-vacancy__top__title", first=True)
		title = block_title.text
		link = block_title.attrs.get("href")
		# Отримуємо всі блоки обернені в тег <b> - перший з них буде зп, а другий компанією

		salary = raw_offer.find(".b-vacancy__top__pay", first=True)
		salary = salary.text if salary else ""

		company = raw_offer.find("div.b-vacancy__tech > span:nth-child(1) > span", first=True).text
		# Отримуємо опис вакансії
		desc = raw_offer.find(".grey-light", first=True)
		desc = desc.text if desc else ""
		# Отримуємо місто на яке розрахована ця ваканція
		city = raw_offer.find("div.b-vacancy__tech > span:nth-child(2) > a", first=True).text

		return OfferModel(
			title=title, city=city if city else None, salary=salary, company=company,
			description=desc, link=link
			)

	def get_count_of_pages(self, url) -> int:
		"""
		Метод який повертає кількість сторінок в пагінації
		"""
		html = self.session.get(url).html
		pagination_block = html.find(".b-vacancy__pages-title", first=True)

		count_of_pages = 1
		if pagination_block:
			count_of_pages = pagination_block.find("b:nth-child(2)", first=True).text
		return int(count_of_pages)







