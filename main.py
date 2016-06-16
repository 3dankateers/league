from summoner import Summoner
from match import Match
from league_client import LeagueClient
from db_client import DbClient
from summoner_parser import SummonerParser
from match_parser import MatchParser
from team_finder import TeamFinder
from champ_parser import ChampParser
from champ_winrate_calculator import ChampWinrateCalculator
from pair_winrate_calculator import PairWinrateCalculator
from comp_analyzer import CompAnalyzer
from test_suite import TestSuite
from one_champ_evaluator import OneChampEvaluator
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

##TODO: Try finding 5v5 games and mark them accordingly
##TODO: Parallel region processing?
##TODO: Add champions to collection
##TODO: Add teams to collection
##TODO: Firstblood idea
##TODO: standardize date to either time.time() or datetime.datetime
##TODO: deal with unicode errors insteadme.encode(encoding='UTF-8',errors='replace') of ignoring
##TODO: Add limits to amount of data pulled and come up with system to pull more efficiently
##TODO: Set patch limits on recent_matches
##TODO: perhaps try finding smurfs statistically
##TODO: get better test data(lcs) or test against 5v5 team games

def main():	
	##pull_summoners("kr", "MASTER")
	##pull_matches("kr", "MASTER")
	##pull_champs()
	##team1 = ["", "", "", "", ""]
	##team2 = ["", "", "", "", ""]
	##team1 = ["Lucian", "Gragas", "Swain", "", ""]
	##team2 = ["Maokai", "Rek'Sai", "Braum", "Ashe", ""]
	##team1 = ["Ryze", "Ekko", "Rek'Sai", "Sivir", "Nami"]
	##team2 = ["Maokai", "Lucian", "Anivia", "Graves", "Soraka"]
	##team1 = ["Kindred", "Alistar", "Ekko", "Ezreal", "LeBlanc"]
	##team2 = ["Zyra", "Lucian", "Lissandra", "Graves", "Kassadin"]
	##team3 = ["Ekko", "Ezreal", "Soraka", "Varus", "Olaf"]
	##team4 = ["Karma", "Rek'Sai", "Maokai", "Sivir", "Fizz"]
	##evaluate_comp(team1, team2)
	##evaluate_comp(team3, team4)
	##new_tests()
	##svm_model = calc_svm_model()
	##evaluate_svm(team1, team2, svm_model)
	##calc_edge(183,-246)
	##SVMTrainer.run()
	##0.2, 0.1, 0.7
	##cross_validate(GeneralEvaluator, 10, "first_blood")
	##new_tests()
	##insert_pro_matches()
	##calc_hyperpoints()
	##ProMatch.print_by_status("nitrogen")
	##ProMatch.print_by_status_tournament("nitrogen", "LSPL")
	##ProMatch.reset_all_tests()
	##calc_hyperpoints()
	##retrain_all("win", premade_only = False)
	##find_teams()
	simulate_bets(OneChampEvaluator, need_confidence = False, premade_only = False)
	simulate_bets(TrivialEvaluator, need_confidence = False, premade_only = False)
	simulate_bets(BayesNetsEvaluator, need_confidence = False, premade_only = False)
	simulate_bets(SVMEvaluator, need_confidence = False, premade_only = False)
	simulate_bets(GeneralEvaluator, need_confidence = False, premade_only = False)
	##simulate_bets(GeneralEvaluator)
	##simulate_bets(AllyPairEvaluator)
	##simulate_bets(EnemyPairEvaluator)
	##simulate_bets(BayesNetsEvaluator)
	##run_tests(EnemyPairEvaluator, ProMatch, "win", need_confidence = False, premade_only = False)
	##run_tests(OneChampEvaluator, ProMatch, "win", need_confidence = False, premade_only = False)
	##run_tests(EnemyPairEvaluator, ProMatch, "frst_blood", need_confidence = False, premade_only = False)
	##run_tests(OneChampEvaluator, ProMatch, "first_blood", need_confidence = False, premade_only = False)
	##train_general_evaluator()

##simulate betting
def simulate_bets(evaluator_class, need_confidence = False, premade_only = False):
	retrain_all("win", premade_only)
	bs = BetSimulator(evaluator_class, need_confidence)
	bs.run()
	bs.print_results()

## run test suite using whatever evaluator class is passed in to predict winners
def run_tests(evaluator_class, match_class, prediction_target, need_confidence, premade_only):
	
	##set new test set and retrain before running tests
	TestSuite.set_new_tests()
	evaluator_class.retrain(prediction_target, premade_only)
	##retrain_all(prediction_target, premade_only)
	
	ts = TestSuite(evaluator_class, match_class, prediction_target, need_confidence)
	ts.run_simple_tests()
	ts.print_results()

def retrain_all(prediction_target, premade_only):
	SVMEvaluator.retrain(prediction_target, premade_only)
	PairEvaluator.retrain(prediction_target, premade_only)
	OneChampEvaluator.retrain(prediction_target, premade_only)

def new_tests():
	TestSuite.set_new_tests()	
	SVMEvaluator.retrain()
	PairEvaluator.retrain()
	OneChampEvaluator.retrain(prediction_target)

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
