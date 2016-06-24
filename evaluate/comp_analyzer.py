############################################################################
## given team comp
## display various metrics to evaluate the team comp
############################################################################

from db_client import DbClient
from champ import Champ
from one_champ_evaluator import OneChampEvaluator
from evaluator import Evaluator
from ally_pair_evaluator import AllyPairEvaluator
from enemy_pair_evaluator import EnemyPairEvaluator
from general_evaluator import GeneralEvaluator
from match_hyperpoint import MatchHyperpoint
from svm_calculator import SVMCalculator
from bayes_nets_evaluator import BayesNetsEvaluator
from kneighbours_evaluator import KNeighboursEvaluator

class CompAnalyzer:
	
	def __init__(self, team1, team2):
		
		self.team1_ids = []
		self.team2_ids = []
		
		##make sure none of the champ names are misspelled
		self.check_team_champ_names(team1, self.team1_ids)
		self.check_team_champ_names(team2, self.team2_ids)

		self.team1_names = team1
		self.team2_names = team2
	
	def evaluate_all(self):
		##self.evaluate_one_champ()
		##self.evaluate_ally_pairs()
		##self.evaluate_enemy_pairs()
		print "Predicting Win"
		self.evaluate_general()
		##self.evaluate_kneighbours()
		self.evaluate_bayes_nets()
		GeneralEvaluator.retrain("win", False)
		
	## checks that champions are spelled properly
	def check_team_champ_names(self, team_names, team_ids):
		for champ_name in team_names:
			cursor = Champ.find_champ_by_name(champ_name)
			champ = Champ.from_dict(cursor[0])
			team_ids.append(champ.id)
			if cursor.count() == 0:
				print "Mistyped champ name: ", champ_name

	def evaluate_one_champ(self):
		one_champ_evaluator = OneChampEvaluator(self.team1_ids, self.team2_ids)
		one_champ_evaluator.process()
		one_champ_evaluator.print_results()
	
	def evaluate_ally_pairs(self):
		pair_evaluator = AllyPairEvaluator(self.team1_ids, self.team2_ids)
		pair_evaluator.process()
		pair_evaluator.print_results()

	def evaluate_enemy_pairs(self):
		pair_evaluator = EnemyPairEvaluator(self.team1_ids, self.team2_ids)
		pair_evaluator.process()
		pair_evaluator.print_results()
	
	def evaluate_general(self):
		evaluator = GeneralEvaluator(self.team1_ids, self.team2_ids)
		evaluator.process()
		evaluator.print_results()
	
	def evaluate_bayes_nets(self):
		evaluator = BayesNetsEvaluator(self.team1_ids, self.team2_ids)
		evaluator.process()
		evaluator.print_results()
	
	def evaluate_kneighbours(self):
		evaluator = KNeighboursEvaluator(self.team1_ids, self.team2_ids)
		evaluator.process()
		evaluator.print_results()
	##def evaluate_svm(self, svm_model):
		##coordinates = MatchHyperpoint.get_coordinates(self.team1_ids, self.team2_ids)
		##print str(svm_model.predict(coordinates))


