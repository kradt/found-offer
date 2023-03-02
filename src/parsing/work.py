from requests_html import HTMLSession
from pydantic import BaseModel
from enum import Enum


class TypeEmployment(Enum):
	FULL = 74
	NOTFULL = 75


class Salary(Enum):
	ANY = 0
	THREE = 2
	FIVE = 3
	SEVEN = 4
	TEN = 5
	FIFTEEN = 6
	TWENTY = 7
	THIRTY = 8
	FIFTY = 9


class SalaryRange(BaseModel):
	FROM: Salary | None
	TO: Salary | None


class WorkUA:
	__link = "https://www.work.ua/{}"

	def __init__(self):
		self.session = HTMLSession()


	def _create_link_by_filters(self,
								city: str | None = None,
								job: str | None = None, 
								type_of_employ: tuple[TypeEmployment] | None = None, 
								category: list[int] | None = None, 
								salary: SalaryRange | None = None) -> str:
		link = self.__link
		filter_block = "jobs"
		if city:
			filter_block += f"-{city}"
		if job:
			filter_block += f"-{job}/"

		# Означає що будуть використувавтися розширені фільтри
		filter_block += "?advs=1"

		#TODO: category handle
		if type_of_employ:
			type_ = "+".join([str(i.value) for i in type_of_employ])
			filter_block += f"&employment={type_}"

		if salary:
			salary_ = ""
			if salary.FROM:
				salary_ += f"&salaryfrom={salary.FROM.value}"
			if salary.TO:
				salary_ += f"&salaryto={salary.TO.value}"
			filter_block += salary_


		return link.format(filter_block)


work = WorkUA()
t_o_e = (TypeEmployment.FULL, TypeEmployment.NOTFULL)
sal = SalaryRange(FROM=Salary.TEN, TO=Salary.FIFTY)
soup = work._create_link_by_filters("kyiv", "backend", t_o_e, salary=sal)
print(soup)