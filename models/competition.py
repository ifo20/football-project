"""
Represents a competition and it's history over many years
"""
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class Competition:
	def __init__(self, slug, name):
		self.slug = slug
		self.name = name
		self.history = [] # list of winners