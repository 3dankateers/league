## Tries different weights with general evaluator to see what works best
from test_suite import TestSuite
from match import Match
from cross_validator import CrossValidator
import random


##stores results from each iteration
class TestResults:
	def __init__(self, one_champ_w, ally_pair_w, enemy_pair_w, performance):
		self.one_champ_w = one_champ_w
		self.ally_pair_w = ally_pair_w
		self.enemy_pair_w = enemy_pair_w
		self.performance = performance

	def tprint(self):
		print "Performance: ", self.performance
		print "One Champ W : ", self.one_champ_w
		print "Ally Pair W : ", self.ally_pair_w
		print "Enemy Pair W : ", self.enemy_pair_w

class GeneralEvaluatorTrainer:
	## 0.2, 0.1, 0.7 ~ 57% on cross validation *10
	## 0.4, 0.3, 0.3 ~ 56% on cross validation *10
	one_champ_w_global = 0.45
	ally_pair_w_global = 0.1
	enemy_pair_w_global = 0.45
	def __init__(self, general_evaluator_class):
		self.general_evaluator_class = general_evaluator_class
		self.number_iterations = 0
		self.all_results = []
		self.past_performance = 0
		
		## set intial values for weighs, will be changed later
		self.w_decrement = 0.20

	##Essentially algorithm tries to optimize weights by doing a variant of randomized hill climbing
	def run(self):
		
		rand_n = random.randint(1, 3)
		for i in range(3):
			for j in range(5):
				print rand_n

				##used to restore weights if there is no improvement
				temp_w1 = GeneralEvaluatorTrainer.one_champ_w_global
				temp_w2 = GeneralEvaluatorTrainer.ally_pair_w_global
				temp_w3 = GeneralEvaluatorTrainer.enemy_pair_w_global
				self.tweak_weights((rand_n%3) + 1)

				cv = CrossValidator(self.general_evaluator_class, Match, 3)
				cv.run()
				performance = cv.get_performance()
				
				##store and print results
				tr = TestResults(GeneralEvaluatorTrainer.one_champ_w_global, GeneralEvaluatorTrainer.ally_pair_w_global, GeneralEvaluatorTrainer.enemy_pair_w_global, performance)
				tr.tprint()
				self.all_results.append(tr)
				
				##if improvement keep changes and update past_performance
				if performance > self.past_performance:
					self.past_performance = performance
				##else restore to previous weights and try again
				else:
					print "Restoring weights"
					self.restore_weights(temp_w1, temp_w2, temp_w3)
				
				
				##over time make changes less volatile
				self.w_decrement -= 0.005
				rand_n += 1

			print "getting new tests"
			##every 5 iterations reset tests
			##cv.set_new_tests()
			##cv.retrain()
	
	def tweak_weights(self, rand_n):
		if rand_n == 1 and (GeneralEvaluatorTrainer.one_champ_w_global - self.w_decrement) > 0:
			GeneralEvaluatorTrainer.one_champ_w_global -= self.w_decrement
			GeneralEvaluatorTrainer.ally_pair_w_global += self.w_decrement/float(2)
			GeneralEvaluatorTrainer.enemy_pair_w_global += self.w_decrement/float(2)
		elif rand_n == 2 and (GeneralEvaluatorTrainer.ally_pair_w_global - self.w_decrement) > 0:
			GeneralEvaluatorTrainer.one_champ_w_global += self.w_decrement/float(2)
			GeneralEvaluatorTrainer.ally_pair_w_global -= self.w_decrement
			GeneralEvaluatorTrainer.enemy_pair_w_global += self.w_decrement/float(2)
		elif rand_n == 3 and (GeneralEvaluatorTrainer.enemy_pair_w_global - self.w_decrement) > 0:
			GeneralEvaluatorTrainer.one_champ_w_global += self.w_decrement/float(2)
			GeneralEvaluatorTrainer.ally_pair_w_global += self.w_decrement/float(2)
			GeneralEvaluatorTrainer.enemy_pair_w_global -= self.w_decrement
	

	def restore_weights(self, w1, w2 ,w3):
		GeneralEvaluatorTrainer.one_champ_w_global = w1
		GeneralEvaluatorTrainer.ally_pair_w_global = w2
		GeneralEvaluatorTrainer.enemy_pair_w_global = w3

	
	def print_results(self):
		for tr in self.all_results:
			tr.tprint()

