import logging
import random
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

next_id = 0

class User:
	def __init__(self, name, dob, height):
		global next_id
		self.id = next_id
		next_id += 1
		self.name = name
		self.dob = dob
		self.height = height

	def __str__(self):
		return self.name
