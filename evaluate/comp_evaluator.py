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
		self.team1_strings = team1
		self.team2_strings = team2
		self.team1_ids = CompEvaluator.get_champ_ids(team1)
		self.team2_ids = CompEvaluator.get_champ_ids(team2)
	
	## take in a list of champ names and return a list of champ ids
	@staticmethod
	def get_champ_ids(team):
		ids = []
		for c in team:
			cursor = Champ.find_champ_by_name(c)
			champ = Champ.from_dict(cursor[0])
			ids.append(champ.id)
		return ids

	
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
		pair_evaluator = PairEvaluator(self.team1_ids, self.team2_ids)
		pair_evaluator.print_results()

