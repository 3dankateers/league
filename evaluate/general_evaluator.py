## Aggregates evaluators
## finds optimal weights to assign

from evaluator import Evaluator
from one_champ_evaluator import OneChampEvaluator
from ally_pair_evaluator import AllyPairEvaluator
from enemy_pair_evaluator import EnemyPairEvaluator
from general_evaluator_trainer import GeneralEvaluatorTrainer 
from pair_winrate_calculator import PairWinrateCalculator
from champ_winrate_calculator import ChampWinrateCalculator
from match import Match
from pro_match import ProMatch
CONF_THRESHOLD = 0.02


class GeneralEvaluator:
	
	##weights are optionally passed in for training exercise
	def __init__(self, champs1_ids, champs2_ids):
		##self.one_champ_w = one_champ_w
		##self.ally_pair_w = ally_pair_w
		##self.enemy_pair_w = enemy_pair_w
		self.one_champ_w = GeneralEvaluatorTrainer.one_champ_w_global
		self.ally_pair_w = GeneralEvaluatorTrainer.ally_pair_w_global
		self.enemy_pair_w = GeneralEvaluatorTrainer.enemy_pair_w_global

		self.one_champ_evaluator = OneChampEvaluator(champs1_ids, champs2_ids)
		self.ally_pair_evaluator = AllyPairEvaluator(champs1_ids, champs2_ids)
		self.enemy_pair_evaluator = EnemyPairEvaluator(champs1_ids, champs2_ids)
		self.champs1_ids = champs1_ids
		self.champs2_ids = champs2_ids
		self.team1_winrate = 0
		self.team2_winrate = 0
	
	@staticmethod
	def retrain(prediction_target, premade_only):
		winrate_calc = PairWinrateCalculator(prediction_target, premade_only)
		winrate_calc.run()
		winrate_calc = ChampWinrateCalculator(prediction_target, premade_only)
		winrate_calc.run()
	
	## return 100 if team1 is favoured, else return 200
	def predict_winner(self):
		return self.winner
	
	def is_confident(self):
		if abs(self.team1_winrate - self.team2_winrate) > CONF_THRESHOLD:
			return True
		else:
			return False
	
	
	def normalize_winrates(self):
		winrate1 = self.team1_winrate
		winrate2 = self.team2_winrate
		##TODO: Return third value idk later for uncertainty
		if (winrate1 + winrate2) > 0:
			self.team1_winrate = winrate1/(winrate1 + winrate2)
			self.team2_winrate = winrate2/(winrate1 + winrate2)

	def print_results(self):
		print "#################################################################################"
		print "General Evaluator Results: "
		print "Team1: ", str(self.team1_winrate)
		print "#########################################################"
		print "Team2: " , str(self.team2_winrate)
		print "Difference: ", self.team1_winrate - self.team2_winrate
		print "WINNER: ", self.winner
		print "#################################################################################"
	
		
	def process(self):
		self.one_champ_evaluator.process()
		self.ally_pair_evaluator.process()
		self.enemy_pair_evaluator.process()
		self.team1_winrate = self.ally_pair_w*self.ally_pair_evaluator.team1_ally_info.aggregate_winrate + self.enemy_pair_w*self.enemy_pair_evaluator.team1_enemy_info.aggregate_winrate + self.one_champ_w*self.one_champ_evaluator.ti1.aggregate_winrate 
		self.team2_winrate = self.ally_pair_w*self.ally_pair_evaluator.team2_ally_info.aggregate_winrate + self.enemy_pair_w*self.enemy_pair_evaluator.team2_enemy_info.aggregate_winrate + self.one_champ_w*self.one_champ_evaluator.ti2.aggregate_winrate 

		self.normalize_winrates()
		if self.team1_winrate > self.team2_winrate:
			self.winner = 100
		else:
			self.winner = 200
