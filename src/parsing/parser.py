from .engines import WorkUA, JobsUA


class Parser:

	def __init__(self, engines: list[object]):
		self.engines = engines



engines = [WorkUA(), JobsUA()]
parser = Parser(engines)

