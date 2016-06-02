from summoner import Summoner
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
	##calc_pair_winrates()
	##calc_champ_winrates()
	##calc_hyperpoints()
	##pull_summoners("BR", "CHALLENGER")
	##pull_matches("BR", "CHALLENGER")
	##pull_champs()
	##team1 = ["Annie", "Alistar", "Ashe", "Braum", "Syndra"]
	##team2 = ["Maokai", "Graves", "Lee Sin", "Ezreal", "Alistar"]
	##evaluate_comp(team1, team2)
	##new_tests()
	##run_tests(SVMEvaluator)
	##svm_model = calc_svm_model()
	##evaluate_svm(team1, team2, svm_model)
	##calc_edge(136,-179)
	##SVMTrainer.run()	
	##cross_validate(SVMEvaluator, 5)
	##insert_pro_matches()
	run_tests(GeneralEvaluator, ProMatch)

## run test suite using whatever evaluator class is passed in to predict winners
def run_tests(evaluator_class, match_class):
	ts = TestSuite(evaluator_class, match_class, False)
	ts.run_simple_tests()
	ts.print_results()

def insert_pro_matches():
	pmc = ProMatchCreator()
	pmc.add_matches()

def cross_validate(evaluator, num_runs):
	cv = CrossValidator(evaluator, num_runs)
	cv.run()
	cv.print_results()

def calc_edge(ml1, ml2):
	EdgeCalculator.analyze_odds(ml1,ml2)

def evaluate_svm(t1, t2, svm_model):
	ca = CompAnalyzer(t1, t2)
	ca.evaluate_svm(svm_model)

def calc_svm_model():
	return SVMCalculator.get_svm_model()

def calc_hyperpoints():
	hc = HyperpointCalculator()
	hc.run()
	

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

def calc_champ_winrates():
	winrate_calc = ChampWinrateCalculator()
	winrate_calc.run()

def calc_pair_winrates():
	winrate_calc = PairWinrateCalculator()
	winrate_calc.run()

def find_teams():
	tf = TeamFinder()
	tf.run()

def evaluate_comp(t1, t2):
	ca = CompAnalyzer(t1,t2)
	ca.evaluate_all()
	##print str(ca.predict_winner())

def new_tests():
	TestSuite.set_new_tests()	
	calc_hyperpoints()
	calc_pair_winrates()
	calc_champ_winrates()



main()
