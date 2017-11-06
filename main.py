from summoner import Summoner
from match import Match
from league_client import LeagueClient
from db_client import DbClient
from champ import Champ
from champ_winrate_calculator import ChampWinrateCalculator
from one_champ_evaluator import OneChampEvaluator
'''
from summoner_parser import SummonerParser
from match_parser import MatchParser
from team_finder import TeamFinder
from champ_parser import ChampParser
from pair_winrate_calculator import PairWinrateCalculator
from comp_analyzer import CompAnalyzer
from test_suite import TestSuite
from ally_pair_evaluator import AllyPairEvaluator
from enemy_pair_evaluator import EnemyPairEvaluator
from trivial_evaluator import TrivialEvaluator
from hyperpoint_calculator import HyperpointCalculator
from svm_calculator import SVMCalculator
from svm_evaluator import SVMEvaluator
from edge_calculator import EdgeCalculator
from cross_validator import CrossValidator
from svm_trainer import SVMTrainer
from pair_evaluator import PairEvaluator
from pro_match_creator import ProMatchCreator
from pro_match import ProMatch
from general_evaluator import GeneralEvaluator
from general_evaluator_trainer import GeneralEvaluatorTrainer
from tree_evaluator import TreeEvaluator
from bayes_nets_evaluator import BayesNetsEvaluator
from bet_simulator import BetSimulator
from odd import Odd
from underdog_evaluator import UnderdogEvaluator
from aggregate_evaluator import AggregateEvaluator
from random_evaluator import RandomEvaluator
from kneighbours_evaluator import KNeighboursEvaluator
from first_blood_evaluator import FirstBloodEvaluator
from loser_evaluator import LoserEvaluator
from trainer import Trainer
##from neural_network_evaluator import NeuralNetworkEvaluator
'''

##TODO: Fix loser evaluator
##TODO: Make neural networks evaluator
##TODO: Get higher resolution betting info + other betting info about fb/ties etc
##TODO: Start grabbing 5v5 data

def main():
    ##DbClient.create_tables()
    ##lc = LeagueClient()
    ##lc.get_challengers("na1")
    ##Summoner.get_summoners_by_tier("CHALLENGER")
    ##lc.get_matches("na1","CHALLENGER")
    ##lc.get_champs("na1")
    ##Champ.reset_winrates()
    ##cwc = ChampWinrateCalculator()
    ##cwc.run()
    oce = OneChampEvaluator([101, 48, 51, 76, 16],[117, 421, 96, 238, 84])
    oce.process()
    oce.print_results()
    ##pull_summoners("eune", "CHALLENGER")
	##pull_matches("eune", "CHALLENGER")
	##pull_champs()
	## NEVER EVER FUCKING EVER BET ON TSM
	##team1 = ["Rek'Sai", "Morgana", "Viktor", "Shen", "Ashe"]
	##team2 = ["Jhin", "Braum", "Cassiopeia", "Graves", "Irelia"]
	##team1 = ["Karma", "Rek'Sai", "Sivir", "Gnar", "Zilean"]
	##team2 = ["Nidalee", "Karma", "Fiora", "Ezreal", "Braum"]
	##evaluate_comp(team1, team2)
	##evaluate_comp(team3, team4)
	##new_tests()
	##svm_model = calc_svm_model()
	##evaluate_svm(team1, team2, svm_model)
	##calc_edge(-122,-106)
	##SVMTrainer.run()
	##0.2, 0.1, 0.7
	##cross_validate(GeneralEvaluator, 10, "first_blood")
	##new_tests()
	##insert_pro_matches()
	##ProMatchCreator.fix_corrupted_matches2()
	##ProMatchCreator.identify_corrupted()
	##calc_hyperpoints()
	##ProMatch.print_by_status("nitrogen")
	##ProMatch.print_by_status_tournament("nitrogen", "Europe")
	#ProMatch.reset_all_tests()
	##calc_hyperpoints()
	##find_teams()
	##simulate_bets(UnderdogEvaluator, need_confidence = False, premade_only = False)
	##simulate_bets(TrivialEvaluator, need_confidence = False, premade_only = False)
	##total = 0
	##wpt = 0
	##for i in range(10):
		##GeneralEvaluator.retrain("win", Trainer.PRO_MATCHES)
		##(wp,profit)= simulate_bets(GeneralEvaluator, need_confidence = False, premade_only = False)
		##total += profit
		##wpt += wp
	##print total/10
	##print wpt/10
	
	##for i in range(10):
	##	retrain_all(Trainer.PRO_MATCHES)
	##	total += simulate_bets(BayesNetsEvaluator, need_confidence = False, premade_only = False)
	##print total/10

	##retrain_all(Trainer.SOLOQ)
	##simulate_bets(LoserEvaluator, need_confidence = True, premade_only = False)
	##simulate_bets(UnderdogEvaluator, need_confidence = False, premade_only = False)
	##simulate_bets(BayesNetsEvaluator, need_confidence = False, premade_only = False)
	##simulate_bets(KNeighboursEvaluator, need_confidence = False, premade_only = False)
	##simulate_bets(AggregateEvaluator, need_confidence = False, premade_only = False)
	##simulate_bets(AggregateEvaluator, need_confidence = True, premade_only = False)
	##simulate_bets(TrivialEvaluator, need_confidence = False, premade_only = False)
	##simulate_bets(RandomEvaluator, need_confidence = False, premade_only = False)
	##simulate_bets(RandomEvaluator, need_confidence = False, premade_only = False)
	##simulate_bets(RandomEvaluator, need_confidence = False, premade_only = False)
	##simulate_bets(RandomEvaluator, need_confidence = False, premade_only = False)
	##simulate_bets(RandomEvaluator, need_confidence = False, premade_only = False)
	##simulate_bets(RandomEvaluator, need_confidence = False, premade_only = False)
	##simulate_bets(UnderdogEvaluator, need_confidence = False, premade_only = False)
	##simulate_bets(GeneralEvaluator, need_confidence = False, premade_only = False)
	##simulate_bets(OneChampEvaluator, need_confidence = False, premade_only = False)
	##simulate_bets(AllyPairEvaluator, need_confidence = False, premade_only = False)
	##simulate_bets(EnemyPairEvaluator, need_confidence = False, premade_only = False)
	##simulate_bets(GeneralEvaluator, need_confidence = True, premade_only = False)
	##simulate_bets(OneChampEvaluator, need_confidence = True, premade_only = False)
	##simulate_bets(AllyPairEvaluator, need_confidence = True, premade_only = False)
	##simulate_bets(EnemyPairEvaluator, need_confidence = True, premade_only = False)
	##simulate_bets(OneChampEvaluator, need_confidence = True, premade_only = False)
	##simulate_bets(AllyPairEvaluator, need_confidence = True, premade_only = False)
	##simulate_bets(EnemyPairEvaluator, need_confidence = True, premade_only = False)
	##simulate_bets(TreeEvaluator, need_confidence = False, premade_only = False)
	##simulate_bets(BayesNetsEvaluator, need_confidence = False, premade_only = False)
	##run_tests(BayesNetsEvaluator, ProMatch, "first_blood", need_confidence = True, premade_only = False)
	##run_tests(OneChampEvaluator, ProMatch, "win", need_confidence = False, premade_only = False)
	##run_tests(EnemyPairEvaluator, ProMatch, "win", need_confidence = False, premade_only = False)
	##run_tests(AllyPairEvaluator, ProMatch, "win", need_confidence = False, premade_only = False)
	##run_tests(TreeEvaluator, ProMatch, "first_blood", need_confidence = False, premade_only = False)
	
	##train_general_evaluator()

##simulate betting
def simulate_bets(evaluator_class, need_confidence = False, premade_only = False):
	evaluator_class.print_class()
	##evaluator_class.retrain("win", premade_only)
	bs = BetSimulator(evaluator_class,  need_confidence)
	bs.run()
	return bs.print_results()

## run test suite using whatever evaluator class is passed in to predict winners
def run_tests(evaluator_class, match_class, prediction_target, need_confidence, premade_only):
	
	##set new test set and retrain before running tests
	##TestSuite.set_new_tests()
	##evaluator_class.retrain(prediction_target, premade_only)
	##retrain_all(prediction_target, premade_only)
	
	ts = TestSuite(evaluator_class, match_class, prediction_target, need_confidence)
	ts.run_simple_tests()
	ts.print_results()
	print ""

def retrain_all(train_set_type):
		Trainer.train(train_set_type, Trainer.ALL)

def train_general_evaluator(prediction_target):
	new_tests(prediction_target)	
	trainer = GeneralEvaluatorTrainer(GeneralEvaluator)
	trainer.run()
	trainer.print_results()

def insert_pro_matches():
	pmc = ProMatchCreator()
	pmc.run()

def cross_validate(evaluator, num_runs, prediction_target):
	cv = CrossValidator(evaluator, Match, prediction_target, num_runs)
	cv.run()
	cv.print_results()

def calc_edge(ml1, ml2):
	EdgeCalculator.analyze_odds(ml1,ml2)

def evaluate_svm(t1, t2, svm_model):
	ca = CompAnalyzer(t1, t2)
	ca.evaluate_svm(svm_model)

def calc_svm_model():
	return SVMCalculator.get_svm_model()

def test_grab(lc):
	c = Summoner.get_one_summoner()
	assert c.count() >= 1, "Trying to initilize summoner model from empty cursor"

	summoner = Summoner.from_dict(c[0])
	SummonerParser.grab_peers(lc, summoner)

def pull_champs():
	lc = LeagueClient("global")
	ChampParser.populate_champ_db(lc)

def pull_summoners(region, tier):
	lc = LeagueClient(region)
	SummonerParser.add_summoners_to_db(lc, tier)

def pull_challengers_peers():
	lc = LeagueClient("na")
	SummonerParser.grab_peers_challenger(lc)

def pull_matches(region, tier):
	lc = LeagueClient(region)
	MatchParser.grab_matches_by_tier(lc, tier)

def find_teams():
	tf = TeamFinder()
	tf.run()

def evaluate_comp(t1, t2):
	ca = CompAnalyzer(t1,t2)
	ca.evaluate_all()
	##print str(ca.predict_winner())

main()
