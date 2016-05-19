############################################################################
## given team comp
## display various metrics to evaluate the team comp
############################################################################

from db_client import DbClient
from champ import Champ
from one_champ_evaluator import OneChampEvaluator
from pair_evaluator import PairEvaluator



class CompEvaluator:
	
	def __init__(self, team1, team2):
		self.team1 = team1
		self.team2 = team2
	
	def evaluate_all(self):
		self.evaluate_one_champ()
		self.evaluate_pairs()

	def evaluate_one_champ(self):
		print "#################################################################################"
		print "One Champ Results: "
		print "Team1"
		OneChampEvaluator.print_one_champ_result(self.team1)
		print "#########################################################"
		print "Team2"
		OneChampEvaluator.print_one_champ_result(self.team2)
		print "#################################################################################"
	
	
	def evaluate_pairs(self):
		pair_evaluator = PairEvaluator(self.team1, self.team2)
		pair_evaluator.print_results()

