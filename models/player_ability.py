import random

class PlayerAbility:
	def __init__(self):
		self.speed = random.randint(70,80)
		self.strength = random.randint(75,80)
		self.passing = random.randint(50,60)
		self.finishing = random.randint(70,80)
		self.heading = random.randint(70,80)
		self.vision = random.randint(70,80)
		self.crossing = random.randint(70,80)
		self.skill = random.randint(70,80)
		self.tackle = random.randint(70,80)
		self.shooting = random.randint(70,80)

	def __repr__(self):
		return f"{self.__dict__}"

	def train(self):
		self.speed += random.randint(0, 2)
		self.strength += random.randint(0, 2)
		self.vision += random.randint(0, 2)
