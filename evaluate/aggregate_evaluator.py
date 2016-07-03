##Aggregates several evaluators into one
##To be used by bet simulator only(if underdog evaluator is used)
## Returns confident only if multiple evaluators agree on winner predicted
## should only be ran with confidence required if want all of them to agree
##TODO consider generalizing this for n evaluators

from one_champ_evaluator import OneChampEvaluator
from enemy_pair_evaluator import EnemyPairEvaluator
from general_evaluator import GeneralEvaluator
from trivial_evaluator import TrivialEvaluator
from underdog_evaluator import UnderdogEvaluator
from evaluator import Evaluator
from trainer import Trainer

class AggregateEvaluator(Evaluator):

	def __init__(self, champ1_ids, champ2_ids, match):
		self.enemy_pair_evaluator = EnemyPairEvaluator(champ1_ids, champ2_ids)
		self.trivial_evaluator = TrivialEvaluator(champ1_ids, champ2_ids, match)
		self.underdog_evaluator = UnderdogEvaluator(match)

		##stores number of times team1 and team2 were predicted to win
		self.team1_num_win = 0
		self.team2_num_win = 0
	
	def process(self):
		self.enemy_pair_evaluator.process()
		self.trivial_evaluator.process()
		self.underdog_evaluator.process()
		
		self.count_winner_predicted(self.enemy_pair_evaluator)
		self.count_winner_predicted(self.underdog_evaluator)
		self.count_winner_predicted(self.trivial_evaluator)

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
		##retrain general evaluator, trivial and underdog do not require retraining
		Trainer.train(train_set_type, Trainer.ALL)

	def is_confident(self):
		if (self.enemy_pair_evaluator.predict_winner() == self.trivial_evaluator.predict_winner()) and (self.trivial_evaluator.predict_winner() == self.underdog_evaluator.predict_winner()):
			return True
		else:
			return False

	def print_results(self):
		print "#################################################################################"
		print "Aggregate Evaluator Results: "
		print "OneChamp Evaluator Winner: ", self.enemy_pair_evaluator.predict_winner()
		print "Trivial Evaluator Winner: ", self.trivial_evaluator.predict_winner()
		print "Underdog Evaluator Winner: ", self.underdog_evaluator.predict_winner()
		print "WINNER: ", self.winner
		print "#################################################################################"

	@staticmethod
	def print_class():
		print "Aggregator Evaluator"




