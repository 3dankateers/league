import json;
import urllib2
from summoner import Summoner
from league_client import LeagueClient
from db_client import DbClient

		
def test_grab():
	with DbClient() as db_client:
		c = db_client.get_one_summoner()
		summoner = Summoner.from_cursor(c)
		LeagueClient.grab_peers(summoner)

def main():
	##data = LeagueClient.get_challanger_data()
	##LeagueClient.extract_challangers(data)
	
	test_grab()

main()
