from db_client import DbClient
from match import Match
from random import randint

## out of how many matches should a test be set
## num_total_tests = ( 1/NUM_TESTS * num_total_matches)
NUM_TESTS = 10

class TestSuite:

	def __init__(self):
		self.tests_passed = 0
		self.tests_failed = 0


	@staticmethod
	def set_new_tests():
		##used to decide which matches are set as tests	
		rand = randint(0,NUM_TESTS)
		
		cursor = Match.get_all_matches()
		num_matches = cursor.count()

		for i in range(num_matches):
			match = Match.from_dict(cursor[i])
			
			## set match as test
			if  i%rand == 0:
				match.is_test = True
				match.save()
			##match is not test
			elif match.is_test == True:
				match.is_test = False
				match.save()
	
	## passed in an evaluator
	## run soloq data tests on evaluator to measure performance
	## print results
	def run_simple_tests(self, evaluator_class):
		cursor = Match.get_all_tests()
		for t in cursor:
			test_match = Match.from_dict(t)
			
			evaluator = evaluator_class(test_match.champs1, test_match.champs2)
			winner_predicted = evaluator.predict_winner()
			actual_winner = test_match.win
			if(winner_predicted == actual_winner):
				self.tests_passed += 1
			else:
				self.tests_failed += 1

		print "Tests Passed: ", self.tests_passed
		print "Tests Failed: ", self.tests_failed
		print "Performance: ", self.tests_passed/(self.tests_passed + self.tests_failed)



