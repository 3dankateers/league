from match_hyperpoint import MatchHyperpoint
from hyperpoint_calculator import HyperpointCalculator
from evaluator import Evaluator
from tree_calculator import TreeCalculator


class TreeEvaluator(Evaluator):

	def __init__(self, team1, team2):
		self.team1_ids = team1
		self.team2_ids = team2
	
	@staticmethod
	def retrain():
		hc = HyperpointCalculator()
		hc.run()
		TreeCalculator.get_new_model()

	def process(self):
		tree_model = TreeCalculator.get_tree_model()
		
		coordinates = MatchHyperpoint.get_coordinates(self.team1_ids, self.team2_ids) 
		
		##returns array of 1 element which should be 100 or 200
		self.winner = tree_model.predict(coordinates)

	def predict_winner(self):
		return self.winner

	def is_confident(self):
		return True	
	
	def print_results(self):
		print "Winner predicted by decison tree is : ", str(self.winner) 
