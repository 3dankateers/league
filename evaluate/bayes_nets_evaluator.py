from match_hyperpoint import MatchHyperpoint
from hyperpoint_calculator import HyperpointCalculator
from evaluator import Evaluator
from bayes_nets_calculator import BayesNetsCalculator
from trainer import Trainer


class BayesNetsEvaluator(Evaluator):

	def __init__(self, team1, team2):
		self.team1_ids = team1
		self.team2_ids = team2
	
	@staticmethod
	def retrain(prediction_target, train_set_type):
		Trainer.train(train_set_type, Trainer.HYPERPOINTS)
		BayesNetsCalculator.get_new_model()

	def process(self):
		bayes_nets_model = BayesNetsCalculator.get_bayes_nets_model()
		
		coordinates = MatchHyperpoint.get_coordinates(self.team1_ids, self.team2_ids) 
		
		##returns array of 1 element which should be 100 or 200
		self.winner = bayes_nets_model.predict(coordinates)

	def predict_winner(self):
		return self.winner

	def is_confident(self):
		return True	
	
	def print_results(self):
		print "Winner predicted by Bayes Nets is : ", str(self.winner) 
	
	@staticmethod
	def print_class():
		print "Bayes Nets Evaluator"
