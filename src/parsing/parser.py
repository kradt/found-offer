from .engines import WorkUA, JobsUA
import Threading


class Parser:

	def __init__(self, engines: list[object]):
		self.engines = engines

	def get_needed_pages(self, city, job) -> list:
		pages = []
		for i in self.engines:
			pages.append(i.get_page(city, job))
		return pages

	def query(
		self, 
		city: str | None = None,
		job: str | None = None):
	pages = self.get_needed_pages(city, job)
	for i in pages:



engines = [WorkUA(), JobsUA()]
parser = Parser(engines)

