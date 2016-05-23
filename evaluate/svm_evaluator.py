############################################################################
## evaluate 2 team comps based on generated svm model 
############################################################################

from evaluator import Evaluator
from db_client import DbClient
from svm_calculator import SVMCalculator
from match_hyperpoint import MatchHyperpoint
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)


class SVMEvaluator(Evaluator):

	def __init__(self, team1, team2):
		self.team1_ids = team1
		self.team2_ids = team2

	def process(self):
		svm_model = SVMCalculator.get_svm_model()
		
		coordinates = MatchHyperpoint.get_coordinates(self.team1_ids, self.team2_ids) 
		
		##returns array of 1 element which should be 100 or 200
		self.winner = svm_model.predict(coordinates)[0]
	
	def predict_winner(self):
		return self.winner
	
	def print_results(self):
		print "Winner predicted by svm is : ", str(self.winner) 



