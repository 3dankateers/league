############################################################################
## passed in a certain type of evaluator, cross validates using the evaluator and prints results 
############################################################################

from test_suite import TestSuite
from match import Match
import random

## fraction of tests from training data will be 1/NUM_TESTS, ie NUM_TESTS = 10 => 1/10 of data is test data
NUM_TESTS = 10

class CrossValidator:

    def __init__(self, evaluator_class, something = 9):
        self.evaluator = evaluator_class
        self.num_runes = something

    def set_new_tests(self):
        ##before assigning new tests, remove all previous ones
        Match.remove_all_tests()
        all_matches = Match.get_training_set()
        
        ##set every (num_tests)th match to a test
        for i,m in enumerate(all_matches):
            if  i%NUM_TESTS == self.num_runes:
                m.is_test = True
                m.update()

    def retrain(self):
        self.evaluator.retrain()

    ## run all tests and aggregate results
    def run(self):
        self.set_new_tests()
        self.evaluator.retrain()
        print "Test"
        ts = TestSuite(self.evaluator)
        ts.run_simple_tests()
        ts.print_results()
