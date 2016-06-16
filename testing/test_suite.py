from db_client import DbClient
from match import Match
from pro_match import ProMatch
from random import randint
import math
import statsmodels.stats.proportion

## out of how many matches should a test be set
## num_total_tests = ( 1/NUM_TESTS * num_total_matches)
NUM_TESTS = 10


class TestSuite:

	## prediction target is either win or first_blood(this is what evaluator will predict and what you test against)
	def __init__(self, evaluator_class, match_class, prediction_target = "win",  need_confidence = False):
		self.match_class = match_class
		self.tests_passed = 0
		self.tests_failed = 0
		self.total_tests = 0
		self.total_confident_tests = 0
		self.evaluator_class = evaluator_class
		self.need_confidence = need_confidence
		self.prediction_target = prediction_target

	@staticmethod
	def set_new_tests():
		##before assigning new tests, remove all previous ones
		Match.remove_all_tests()
		
		##used to decide which matches are set as tests	
		rand = randint(0,NUM_TESTS)
		
		cursor = Match.get_testable_set()
		num_matches = cursor.count()

		for i in range(num_matches):
			match = Match.from_dict(cursor[i])

			## set match as test
			if  i%NUM_TESTS == rand:
				##num_tests+= 1
				match.is_test = True
				match.save()


		##used to train with pro matches, sketchy as fuck, commented out for now

		##set half of pro matches to tests half training
#		cursor = ProMatch.get_testable_set()
#		num_matches = cursor.count()
#		for i in range(num_matches):
#			rand = randint(1,2)
#			match = ProMatch.from_dict(cursor[i])
#
#			## set match as test
#			if  rand == 1:
#				##num_tests+= 1
#				match.is_test = True
#				match.save()
#			##match is not test
#			elif rand == 2:
#				##num_non_tests += 1
#				match.is_test = False
#				match.save()
		
		##print "matches :", str(num_matches)
		##print "no tests: ", str(num_non_tests)
		##print "tests: ", str(num_tests)

	
	## passed in an evaluator
	## run soloq data tests on evaluator to measure performance
	## print results
	def run_simple_tests(self):
		cursor = self.match_class.get_test_set()
		for t in cursor:
			test_match = self.match_class.from_dict(t)
			evaluator = self.evaluator_class(test_match.champs1, test_match.champs2)
			evaluator.process()
			##only count test matches if either confidence is not needed( if it is make sure evaluator is confident)
			if((not self.need_confidence) or evaluator.is_confident()):
				self.total_confident_tests += 1
				winner_predicted = evaluator.predict_winner()
				
				
				## test against win or first blood
				if self.prediction_target == Match.WIN:
					actual_winner = test_match.win
				else:
					##make sure test_match actually has first blood info
					if test_match.first_blood != None:
						actual_winner = test_match.first_blood
					else:
						continue
				
				
				if(winner_predicted == actual_winner):
					self.tests_passed += 1
				else:
					self.tests_failed += 1
		self.performance = self.tests_passed/float(self.tests_passed + self.tests_failed)
		self.total_tests = self.tests_passed + self.tests_failed
		return self.performance
	
	def print_confidence_interval(self):
		##mean = self.tests_passed/float(self.total_tests)
		####standard_error = math.sqrt(mean*(1-mean)/float(self.total_tests))
		##large sample using Z distribution
		if (self.total_tests > 1):
				interval = statsmodels.stats.proportion.proportion_confint(self.tests_passed, self.total_tests, alpha=0.05, method='beta')
				low_conf = interval[0] 
				high_conf = interval[1] 
				print "Confidence Interval: [", low_conf, " , ", high_conf, "]"
		else:
			pass

	def retrain(self):
		self.evaluator_class.retrain(self.prediction_target)



	##print results of running tests
	def print_results(self):
		print "Tests Passed: ", self.tests_passed
		print "Tests Failed: ", self.tests_failed
		print "Performance: ", self.performance 
		self.print_confidence_interval()
	
	def get_performance(self):
		return self.performance

