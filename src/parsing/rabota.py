from requests_html import HTMLSession

from models import TypeEmploymentRabota


class RabotaUA:
	__url = "https://rabota.ua/ua/{}"

	def __init__(self):
		self.session = HTMLSession()

	def _create_link_by_filters(
			self,
			city: str | None = None,
			job: str | None = None,
			type_of_employ: tuple[TypeEmploymentRabota] | None = None,
			salary_from: int | None = None) -> str:
		"""
		Метод який створює ссилку по потрібним фільтрам 
		"""
		filter_block = ""
		filter_block += f"zapros/{job}/" if job else ""
		filter_block += f"{city}?" if city  else "" # and if city in dataclass with cities
		filter_block += f"salary={salary_from}" if salary_from else ""# and if salary in range
		return self.__url.format(filter_block)





r = RabotaUA()

job = "backend"
city = "киев"
lnk = r._create_link_by_filters(city=city, job=job)

print(lnk)
		

