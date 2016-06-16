##Aggregates several evaluators into one
##To be used by bet simulator only(if underdog evaluator is used)
## Returns confident only if multiple evaluators agree on winner predicted
## should only be ran with confidence required

from one_champ_evaluator import OneChampEvaluator
from general_evaluator import GeneralEvaluator
from trivial_evaluator import TrivialEvaluator
from underdog_evaluator import UnderdogEvaluator
from evaluator import Evaluator


class AggregateEvaluator(Evaluator):

	def __init__(self, champ1_ids, champ2_ids, match):
		self.one_champ_evaluator = OneChampEvaluator(champ1_ids, champ2_ids)
		self.trivial_evaluator = TrivialEvaluator(champ1_ids, champ2_ids)
		self.underdog_evaluator = UnderdogEvaluator(match)
	
	def process(self):
		self.one_champ_evaluator.process()
		self.trivial_evaluator.process()
		self.underdog_evaluator.process()
		self.winner = self.one_champ_evaluator.predict_winner()
	
	def predict_winner(self):
		return self.winner

	
	@staticmethod
	def retrain(prediction_target, premade_only):
		##retrain general evaluator, trivial and underdog do not require retraining
		OneChampEvaluator.retrain(prediction_target, premade_only)

	def is_confident(self):
		if (self.one_champ_evaluator.predict_winner() == self.trivial_evaluator.predict_winner()) and (self.trivial_evaluator.predict_winner() == self.underdog_evaluator.predict_winner()):
			return True
		else:
			return False

	def print_results(self):
		print "#################################################################################"
		print "Aggregate Evaluator Results: "
		print "OneChamp Evaluator Winner: ", self.one_champ_evaluator.predict_winner()
		print "Trivial Evaluator Winner: ", self.trivial_evaluator.predict_winner()
		print "Underdog Evaluator Winner: ", self.underdog_evaluator.predict_winner()
		print "WINNER: ", self.winner
		print "#################################################################################"

			





