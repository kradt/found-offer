from engines import WorkUA, JobsUA


class Parser:

	def __init__(self, engines:list[object]):
		self.engines = engines

	def create_page(self, city: str, job: str):
		pages = []
		for i in self.engines:
			pages.append(i.get_page(city=city, job=job))
		self.pages = pages

	def paginate(self, per_page, page):
		if not self.pages:
			raise ValueError("You must create page before this")
		offers = []
		for i in self.pages:
			pass







engines = [WorkUA(), JobsUA()]
parser = Parser(engines)
