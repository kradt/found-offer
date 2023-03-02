from requests_html import HTMLSession
from enum import Enum


class TypeEmployment(Enum):
	FULL = 74
	NOTFULL = 75


class WorkUA:
	__link = "https://www.work.ua/{}"

	def __init__(self):
		self.session = HTMLSession()


	def _create_link_by_filters(self,
								city: str | None = None,
								job: str | None = None, 
								type_of_employ: tuple[TypeEmployment] | None = None, 
								category: list[int] | None = None, 
								salary: tuple[int, int] | None = None) -> str:
		link = self.__link
		filter_block = "jobs"
		if city:
			filter_block += f"-{city}"
		if job:
			filter_block += f"-{job}/"

		filter_block += "?advs=1"

		#TODO: category handle
		if type_of_employ:
			type_ = "+".join([str(i.value) for i in type_of_employ])
			filter_block += f"&employment={type_}"

		return link.format(filter_block)


work = WorkUA()
t_o_e = (TypeEmployment.FULL, TypeEmployment.NOTFULL)
soup = work._create_link_by_filters("kyiv", "backend", t_o_e)
print(soup)