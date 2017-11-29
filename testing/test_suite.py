from db_client import DbClient
from match import Match
import math

## out of how many matches should a test be set
## num_total_tests = ( 1/NUM_TESTS * num_total_matches)

class TestSuite:

    ## prediction target is either win or first_blood(this is what evaluator will predict and what you test against)
    def __init__(self, evaluator_class):
        self.tests_passed = 0
        self.tests_failed = 0
        self.total_tests = 0
        self.evaluator_class = evaluator_class

    ## passed in an evaluator
    ## run soloq data tests on evaluator to measure performance
    ## print results
    def run_simple_tests(self):
        self.evaluator_class.print_class()
        test_matches = Match.get_test_set()
        for tm in test_matches:
            evaluator = self.evaluator_class(tm.champs1, tm.champs2)
            evaluator.process()
            winner_predicted = evaluator.predict_winner()
            actual_winner = tm.win
            if(winner_predicted == 0):##0 means no opinion (low confidence)
                pass
            elif(winner_predicted == actual_winner):
                self.tests_passed += 1
            elif(winner_predicted != actual_winner):
                self.tests_failed += 1
        self.performance = self.tests_passed/float(self.tests_passed + self.tests_failed)
        self.total_tests = self.tests_passed + self.tests_failed
        return self.performance
    



    ##print results of running tests
    def print_results(self):
        print "Tests Passed: ", self.tests_passed
        print "Tests Failed: ", self.tests_failed
        print "Performance: ", self.performance 
        print "Prediction %: ", float(self.tests_passed+self.tests_failed)/self.total_tests 
    
    def get_performance(self):
        return self.performance

