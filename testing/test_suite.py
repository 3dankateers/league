from db_client import DbClient
from match import Match
from random import randint

## out of how many matches should a test be set
## num_total_tests = ( 1/NUM_TESTS * num_total_matches)
NUM_TESTS = 10

class TestSuite:

	def __init__(self, evaluator_class, need_confidence = False):
		self.tests_passed = 0
		self.tests_failed = 0
		self.total_tests = 0
		self.total_confident_tests = 0
		self.evaluator_class = evaluator_class
		self.need_confidence = need_confidence



	@staticmethod
	def set_new_tests():
		##used to decide which matches are set as tests	
		rand = randint(0,NUM_TESTS)
		
		cursor = Match.get_all_matches()
		num_matches = cursor.count()
		##num_tests = 0
		##num_non_tests = 0
		##print "Num matches: ", num_matches

		for i in range(num_matches):
			match = Match.from_dict(cursor[i])

			## set match as test
			if  i%NUM_TESTS == rand:
				##num_tests+= 1
				match.is_test = True
				match.save()
			##match is not test
			elif match.is_test == True:
				##num_non_tests += 1
				match.is_test = False
				match.save()
		##print "matches :", str(num_matches)
		##print "no tests: ", str(num_non_tests)
		##print "tests: ", str(num_tests)

	
	## passed in an evaluator
	## run soloq data tests on evaluator to measure performance
	## print results
	def run_simple_tests(self):
		cursor = Match.get_test_set()
		self.total_tests = cursor.count()
		for t in cursor:
			test_match = Match.from_dict(t)
			
			evaluator = self.evaluator_class(test_match.champs1, test_match.champs2)
			evaluator.process()
			##only count test matches if either confidence is not needed( if it is make sure evaluator is confident)
			if((not self.need_confidence) or evaluator.is_confident()):
				self.total_confident_tests += 1
				winner_predicted = evaluator.predict_winner()
				actual_winner = test_match.win
				if(winner_predicted == actual_winner):
					self.tests_passed += 1
				else:
					self.tests_failed += 1
		self.performance = self.tests_passed/float(self.tests_passed + self.tests_failed)
		return self.performance

	##print results of running tests
	def print_results(self):
		print "Tests Passed: ", self.tests_passed
		print "Tests Failed: ", self.tests_failed
		print "Performance: ", self.performance 


