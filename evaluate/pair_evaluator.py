############################################################################
## evaluate 2 team comps based on both ally pairs and enemy pairs 
############################################################################
from ally_pair_evaluator import AllyPairEvaluator
from enemy_pair_evaluator import EnemyPairEvaluator
from pair_winrate_calculator import PairWinrateCalculator
from trainer import Trainer

CONF_THRESHOLD = 0.05

class PairEvaluator:
	def __init__(self, team1, team2):
		self.ally_evaluator = AllyPairEvaluator(team1, team2)
		self.enemy_evaluator = EnemyPairEvaluator(team1, team2)
		self.team1_winrate = 0
		self.team2_winrate = 0


		##weight values to give to each sub evaluator
		##might needs adjustment
		self.w1 = 0.5
		self.w2 = 0.5

	
	@staticmethod
	def retrain(prediction_target, train_set_type):
		Trainer.train(train_set_type, Trainer.PAIR)
		winrate_calc = PairWinrateCalculator(prediction_target, premade_only)
		winrate_calc.run()

	def process(self):
		self.ally_evaluator.process()
		self.enemy_evaluator.process()
		self.team1_winrate = self.w1*self.ally_evaluator.team1_ally_info.aggregate_winrate + self.w2*self.enemy_evaluator.team1_enemy_info.aggregate_winrate
		self.team2_winrate = self.w1*self.ally_evaluator.team2_ally_info.aggregate_winrate + self.w2*self.enemy_evaluator.team2_enemy_info.aggregate_winrate
		self.normalize_winrates()
		if self.team1_winrate > self.team2_winrate:
			self.winner = 100
		else:
			self.winner = 200

	def predict_winner(self):
		return self.winner


	def normalize_winrates(self):
		winrate1 = self.team1_winrate
		winrate2 = self.team2_winrate
		self.team1_winrate = winrate1/(winrate1 + winrate2)
		self.team2_winrate = winrate2/(winrate1 + winrate2)
	
	
	def is_confident(self):
		if abs(self.team1_winrate - self.team2_winrate) > CONF_THRESHOLD:
			return True
		else:
			return False

	def print_results(self):
		print("Ally + Enemy aggregate results:")
		print("Team1 winrate: ", self.team1_winrate)
		print("Team2 winrate: ", self.team2_winrate)
	
	@staticmethod
	def print_class():
		print("Pair Evaluator")
