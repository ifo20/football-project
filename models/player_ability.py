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
		"""Formatted list of abilities"""
		lines = [
			f"{'Attribute':^20}{'Skill':^3}",
		]
		for attribute, value in self.__dict__.items():
			lines.append(f"{attribute.title():20} {value:>3}")
		return "\n".join(lines)

	def train(self):
		self.speed += random.randint(0, 2)
		self.strength += random.randint(0, 2)
		self.vision += random.randint(0, 2)

if __name__ == "__main__":
	print(PlayerAbility())
