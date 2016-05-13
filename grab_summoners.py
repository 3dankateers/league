from summoner import Summoner
from league_client import LeagueClient
from db_client import DbClient
from summoner_processor import SummonerProcessor
from match_processor import MatchProcessor
		
def test_grab():
	with DbClient() as db_client:
		c = db_client.get_one_summoner()
		assert c.count() >= 1, "Trying to initilize summoner model from empty cursor"

		summoner = Summoner.from_object(c[0])
		SummonerProcessor.grab_peers(summoner)

def main():
	
	SummonerProcessor.add_challengers_to_db()
	##test_grab()
	##SummonerProcessor.grab_peers_challenger()


main()
