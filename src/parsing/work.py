from requests_html import HTMLSession


class WorkUA:
	__link = "https://www.work.ua/{}"

	def __init__(self):
		self.session = HTMLSession()


	def _create_link_by_filters(self,
								 city: str | None = None,
								 job: str | None = None, 
								 category: list[int] | None = None, 
								 type_of_employ: list[int] | None = None, 
								 salary: tuple[int, int] | None = None) -> str:
		link = self.__link
		job_block = "jobs"
		if city:
			job_block += f"-{city}"
		if job:
			job_block += f"-{job}"

		return link.format(job_block)


	



work = WorkUA()
soup = work._create_link_by_filters("kiev", "backend")
print(soup)