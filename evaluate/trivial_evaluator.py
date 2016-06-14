##Always return purple side wins
from evaluator import Evaluator

class TrivialEvaluator(Evaluator):
	def __init__(self, champs1_ids, champs2_ids):
		self.winner = 200

	def process(self):
		pass

	def predict_winner(self):
		return self.winner

	def is_confident(self):
		return True

	@staticmethod
	def retrain(prediction_target):
		pass

	def print_results(self):
		print "Trivial Evaluator"
		print "Predicting team 200 wins (purple side)"
