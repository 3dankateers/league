############################################################################
## evaluate 2 team comps based on generated svm model 
############################################################################

from evaluator import Evaluator
from db_client import DbClient
from svm_calculator import SVMCalculator
from match_hyperpoint import MatchHyperpoint
from hyperpoint_calculator import HyperpointCalculator
from trainer import Trainer
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)


CONF_THRESHOLD = 0.10

class SVMEvaluator(Evaluator):

	def __init__(self, team1, team2):
		self.team1_ids = team1
		self.team2_ids = team2
	
	@staticmethod
	def retrain(prediction_target, train_set_type):
		Trainer.train(train_set_type, Trainer.HYPERPOINTS)
		SVMCalculator.get_new_model()

	def process(self):
		svm_model = SVMCalculator.get_svm_model()
		
		coordinates = MatchHyperpoint.get_coordinates(self.team1_ids, self.team2_ids) 
		
		##returns array of 1 element which should be 100 or 200
		##self.winner = svm_model.predict(coordinates)[0]
		self.winner = svm_model.predict(coordinates)
		

	def predict_winner(self):
		print(self.winner)
		return self.winner

	def is_confident(self):
			return True
	
	def print_results(self):
		print("Winner predicted by svm is : ", str(self.winner))

	@staticmethod
	def print_class():
		print("SVM Evaluator")
