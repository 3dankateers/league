## Aggregates several evaluators into one
## To be used by bet simulator only(if underdog evaluator is used)
## Returns confident only if multiple evaluators agree on winner predicted
## Should only be ran with confidence required if want all of them to agree
## TODO consider generalizing this for n evaluators

from one_champ_evaluator import OneChampEvaluator
from enemy_pair_evaluator import EnemyPairEvaluator
from evaluator import Evaluator
from trainer import Trainer

class FirstBloodEvaluator(Evaluator):

	def __init__(self, champ1_ids, champ2_ids):
		self.one_champ_evaluator = OneChampEvaluator(champ1_ids, champ2_ids)
		self.enemy_pair_evaluator = EnemyPairEvaluator(champ1_ids, champ2_ids)

		##stores number of times team1 and team2 were predicted to win
		self.team1_num_win = 0
		self.team2_num_win = 0
	
	def process(self):
		self.one_champ_evaluator.process()
		self.enemy_pair_evaluator.process()
	
		self.count_winner_predicted(self.one_champ_evaluator)
		self.count_winner_predicted(self.enemy_pair_evaluator)

		if self.team1_num_win >= self.team2_num_win:
			self.winner = 100
		else:
			self.winner = 200
	
	def predict_winner(self):
		return self.winner

	##increments team1_win or team_2 win depending on the winner predicted by evaluator passed in
	def count_winner_predicted(self, evaluator):
		if evaluator.predict_winner() == 100:
			self.team1_num_win += 1
		else:
			self.team2_num_win += 1

	@staticmethod
	def retrain(prediction_target, train_set_type):
		Trainer.train(train_set_type, Trainer.ALL)

	def is_confident(self):
		if (self.one_champ_evaluator.predict_winner() == self.enemy_pair_evaluator.predict_winner()):
			return True
		else:
			return False

	def print_results(self):
		print "#################################################################################"
		print "Aggregate Evaluator Results: "
		print "OneChamp Evaluator Winner: ", self.one_champ_evaluator.predict_winner()
		print "EnemyPair Evaluator Winner: ", self.enemy_pair_evaluator.predict_winner()
		print "WINNER: ", self.winner
		print "#################################################################################"
	
	@staticmethod
	def print_class():
		print "First Blood Evaluator"
