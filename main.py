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
from pair_evaluator import PairEvaluator

##TODO: Try finding 5v5 games and mark them accordingly
##TODO: Parallel region processing?
##TODO: Add champions to collection
##TODO: Add teams to collection
##TODO: Firstblood idea
##TODO: standardize date to either time.time() or datetime.datetime
##TODO: deal with unicode errors insteadme.encode(encoding='UTF-8',errors='replace') of ignoring
##TODO: Add limits to amount of data pulled and come up with system to pull more efficiently
##TODO: Set patch limits on recent_matches
## perhaps try finding smurfs statistically

def main():
	##calc_pair_winrates()
	##calc_champ_winrates()
	##pull_challengers("kr")
	##pull_matches("kr")
	##team1 = ["Annie", "Alistar", "Ashe", "Braum", "Syndra"]
	##team2 = ["Maokai", "Graves", "Lee Sin", "Ezreal", "Alistar"]
	##evaluate_comp(team1, team2)
	run_tests()


def test_grab(lc):
	c = Summoner.get_one_summoner()
	assert c.count() >= 1, "Trying to initilize summoner model from empty cursor"

	summoner = Summoner.from_dict(c[0])
	SummonerParser.grab_peers(lc, summoner)

def pull_champs():
	lc = LeagueClient("global")
	ChampParser.populate_champ_db(lc)

def pull_challengers(region):
	lc = LeagueClient(region)
	SummonerParser.add_challengers_to_db(lc)

def pull_challengers_peers():
	lc = LeagueClient("na")
	SummonerParser.grab_peers_challenger(lc)

def pull_matches(region):
	lc = LeagueClient(region)
	MatchParser.grab_matches_challenger(lc)

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

def run_tests():
	TestSuite.set_new_tests()	
	ts = TestSuite()
	ts.run_simple_tests(OneChampEvaluator)

main()
