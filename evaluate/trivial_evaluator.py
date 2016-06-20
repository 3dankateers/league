##Always return purple side wins
from evaluator import Evaluator

class TrivialEvaluator(Evaluator):
	def __init__(self, champs1_ids, champs2_ids, match = None):
		self.match = match

	def process(self):
		if self.match != None:
			self.winner = self.match.red_side
		else:
			self.winner = 100

	def predict_winner(self):
		return self.winner

	def is_confident(self):
		return True

	@staticmethod
	def retrain(prediction_target, premade_only):
		pass

	def print_results(self):
		print "Trivial Evaluator"
		print "Predicting team 200 wins (purple side)"
