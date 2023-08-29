from abc import ABC, abstractmethod
from requests_html import HTMLSession, Element
from .models import OfferModel


class PageQuery(ABC):
	"""
		Interface for parser with page iteration
	"""
	_url = ...
	_offer_classname = ...
	_offers_pattern = ...
	_next_page_pattern = ...

	def __init__(self, current_page: int = 1) -> None:
		self.session = HTMLSession()
		self.current_page = current_page
		self.count_of_pages = self._get_count_of_pages()

	@abstractmethod
	def _is_offer_element(self, elem: Element) -> bool:
		pass

	@abstractmethod
	def _prepare_offer(self, raw_offer: Element) -> OfferModel:
		pass

	@abstractmethod
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