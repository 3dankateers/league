from summoner import Summoner
from league_client import LeagueClient
from db_client import DbClient
from summoner_parser import SummonerParser
from match_parser import MatchParser
from team_finder import TeamFinder
from champ_parser import ChampParser
from champ_winrate_calculator import ChampWinrateCalculator
##TODO: Try finding 5v5 games and mark them accordingly
##TODO: Parallel region processing?
##TODO: Add champions to collection
##TODO: Add teams to collection
##TODO: Firstblood idea
##TODO: standardize date to either time.time() or datetime.datetime
## perhaps try finding smurfs statistically

def main():
	calc_champ_winrates()
	##pull_champs()

def test_grab(lc):
	with DbClient() as db_client:
		c = db_client.get_one_summoner()
		assert c.count() >= 1, "Trying to initilize summoner model from empty cursor"

		summoner = Summoner.from_dict(c[0])
		SummonerParser.grab_peers(lc, summoner)

def pull_champs():
	lc = LeagueClient("global")
	ChampParser.populate_champ_db(lc)

def pull_challengers():
	lc = LeagueClient("na")
	SummonerParser.add_challengers_to_db(lc)

def pull_challengers_peers():
	lc = LeagueClient("na")
	SummonerParser.grab_peers_challenger(lc)

def pull_matches():
	lc = LeagueClient("na")
	MatchParser.grab_matches_challenger(lc)

def calc_champ_winrates():
	winrate_calc = ChampWinrateCalculator()
	winrate_calc.run()

def find_teams():
	tf = TeamFinder()
	tf.run()


main()
