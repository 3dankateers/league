from abc import ABCMeta, abstractmethod
from champ import Champ

## abstract evaluator class that all evaluators inherit from
class Evaluator:
	__metaclass__ = ABCMeta

	@abstractmethod
	def process(self): pass
	def predict_winner(self): pass
	def print_results(self): pass

	## take in a list of champ names and return a list of champ ids
	@staticmethod
	def get_champ_ids(team):
		ids = []
		for c in team:
			cursor = Champ.find_champ_by_name(c)
			champ = Champ.from_dict(cursor[0])
			ids.append(champ.id)
		return ids
