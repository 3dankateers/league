## Aggregates evaluators
## finds optimal weights to assign

from evaluator import Evaluator
from one_champ_evaluator import OneChampEvaluator
from ally_pair_evaluator import AllyPairEvaluator
from enemy_pair_evaluator import EnemyPairEvaluator

CONF_THRESHOLD = 0.05


class GeneralEvaluator:
	
	##weights are optionally passed in for training exercise
	def __init__(self, champs1_ids, champs2_ids, one_champ_w = 0.4, ally_pair_w = 0.3, enemy_pair_w = 0.3):
		self.one_champ_w = one_champ_w
		self.ally_pair_w = ally_pair_w
		self.enemy_pair_w = enemy_pair_w

		self.number_iterations = 0
		self.one_champ_evaluator = OneChampEvaluator(champs1_ids, champs2_ids)
		self.ally_pair_evaluator = AllyPairEvaluator(champs1_ids, champs2_ids)
		self.enemy_pair_evaluator = EnemyPairEvaluator(champs1_ids, champs2_ids)
		self.champs1_ids = champs1_ids
		self.champs2_ids = champs2_ids
		self.team1_winrate = 0
		self.team2_winrate = 0
	
	@staticmethod
	def retrain():
		winrate_calc = PairWinrateCalculator()
		winrate_calc.run()
		winrate_calc = ChampWinrateCalculator()
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
		self.team1_winrate = winrate1/(winrate1 + winrate2)
		self.team2_winrate = winrate2/(winrate1 + winrate2)

	def print_results(self):
		print "Ally + Enemy aggregate results:"
		print "Team1 winrate: ", self.team1_winrate
		print "Team2 winrate: ", self.team2_winrate
	
		
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
