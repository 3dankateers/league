##evaluator simply return 100 or 200 randomly, used for testing purposes

from evaluator import Evaluator
from random import randint

class RandomEvaluator(Evaluator):
	def __init__(self, champs1, champs2):
		pass

	@staticmethod
	def retrain(prediction_target, premade_only):
		pass
	
	def predict_winner(self):
		return self.winner

	def process(self):
		rand = randint(1,2)
		self.winner = rand*100

	def is_confident(self):
		return True

	def print_results(self):
		pass

	@staticmethod
	def print_class():
		print("Random Evaluator")
