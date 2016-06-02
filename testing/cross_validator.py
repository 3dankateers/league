############################################################################
## passed in a certain type of evaluator, cross validates using the evaluator and prints results 
## aggregate testing results by cross validating 
############################################################################

from test_suite import TestSuite
from match import Match

## fraction of tests from training data will be 1/NUM_TESTS, ie NUM_TESTS = 10 => 1/10 of data is test data
NUM_TESTS = 10
##if true, only evaluate predictions given with confidence 
NEED_CONFIDENCE = True

class CrossValidator:

	def __init__(self, evaluator_class, num_runs = NUM_TESTS):
		self.evaluator = evaluator_class
		## number of times tests were ran
		self.num_runs = num_runs
		##used for checking if match should be a test. 
		##if match_num % NUM_TESTS == test_checker then it is a test otherwise it's training data
		self.test_checker = 0
		self.total_performance = 0
		self.normalized_performance = 0
		self.total_tests = 0
		self.total_confident_tests = 0

	def get_performance(self):
		self.calc_performance()
		return self.normalized_performance

	def print_results(self):
		print "Performance calculated by cross validation is:", self.get_performance()
		print "Total Tests: ", self.total_tests
		print "Confident Tests: ", self.total_confident_tests
		print "Confident Percentage = ", str(self.total_confident_tests/float(self.total_tests))
	
	def calc_performance(self):
		self.normalized_performance = self.total_performance/self.num_runs

	
	def set_new_tests(self):
		cursor = Match.get_all_matches()
		num_matches = cursor.count()
		for i in range(num_matches):
			match = Match.from_dict(cursor[i])

			## set match as test
			if  i%NUM_TESTS == self.test_checker:
				##num_tests+= 1
				match.is_test = True
				match.save()
			##match is not test
			elif match.is_test == True:
				##num_non_tests += 1
				match.is_test = False
				match.save()

		##set test_checker to be ready for consecutive calls to set_new_tests
		self.test_checker += 1
	
	## run all tests and aggregate results
	def run(self):
		for i in range(self.num_runs):
			self.set_new_tests()
			self.evaluator.retrain()
			ts = TestSuite(self.evaluator, Match, NEED_CONFIDENCE)
			performance = ts.run_simple_tests()
			self.total_performance += performance
			self.total_tests += ts.total_tests
			self.total_confident_tests += ts.total_confident_tests

			print "Estimated Performance after", (i+1), " runs:"
			print str(self.total_performance/(i+1))