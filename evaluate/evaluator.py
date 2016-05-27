from abc import ABCMeta, abstractmethod
from champ import Champ

## abstract evaluator class that all evaluators inherit from
class Evaluator:
	__metaclass__ = ABCMeta

	@abstractmethod
	
	## process team comp and update stats calculated
	def process(self): pass

	@abstractmethod
	## use processing results to decide if team 1 or team 2 is more likely to win, return 1 or 2
	def predict_winner(self): pass

	@abstractmethod
	## print summary of results calculated
	def print_results(self): pass
	
	@abstractmethod
	## recalculate values used to train model(presumably called after tests were changed)
	def retrain(): pass

	@abstractmethod
	## returns True if evaluator is confident in predicted winner
	def is_confident(self): pass

	## take in a list of champ names and return a list of champ ids
	@staticmethod
	def get_champ_ids(team):
		ids = []
		for c in team:
			cursor = Champ.find_champ_by_name(c)
			champ = Champ.from_dict(cursor[0])
			ids.append(champ.id)
		return ids
