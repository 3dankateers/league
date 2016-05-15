from summoner import Summoner
from league_client import LeagueClient
from db_client import DbClient
from summoner_processor import SummonerProcessor
from match_processor import MatchProcessoruu
from team_finder import TeamFinder

##TODO: Try finding 5v5 games and mark them accordingly
##TODO: Parallel region processing?
##TODO: Add champions to collection
##TODO: Add teams to collection
##TODO: Firstblood idea
##TODO: standardize date to either time.time() or datetime.datetime
## perhaps try finding smurfs statistically

def test_grab(lc):
	with DbClient() as db_client:
		c = db_client.get_one_summoner()
		assert c.count() >= 1, "Trying to initilize summoner model from empty cursor"

		summoner = Summoner.from_dict(c[0])
		SummonerProcessor.grab_peers(lc, summoner)

def main():
	lc = LeagueClient("na")
	##SummonerProcessor.add_challengers_to_db(lc)
	##test_grab(lc)
	##SummonerProcessor.grab_peers_challenger(lc)
	MatchProcessor.grab_matches_challenger(lc)

main()
