########################################################################
## parses data from league_client
## inserts new data into db
########################################################################

import datetime
import time
from summoner import Summoner, tier_converter
from db_client import DbClient
from league_client import LeagueClient

SCRAPE_RESET_DAYS = 10

class Processor:

	##add all challangers to db
	@staticmethod
	def add_challengers_to_db():
		print "Adding all challengers to db..."
		data = LeagueClient.get_challanger_data()
		Processor.populate_challengers(data)


	## populate db with all challangers given data
	@staticmethod
	def populate_challengers(data):
		summoners = data["entries"]
		for s in summoners:
			name = s["playerOrTeamName"]
			league_id = s["playerOrTeamId"]
			division = s["division"]
			tier = "CHALLENGER"
			s_model = Summoner.get_summoner(name, league_id, tier, division)
			s_model.save()
	
	##given recent match data, return list of peers ids
	@staticmethod
	def extract_peers_ids(data):
		peer_ids = []
		games = data["games"]
		print "got here"	
		for g in games:

		##only care about ranked 5v5 games
			if (g["gameType"] == "MATCHED_GAME") and (g["subType"] == "RANKED_SOLO_5x5"):
				peers = g["fellowPlayers"]
				for p in peers:
					s_id = p["summonerId"]
					peer_ids.append(s_id)
		return peer_ids

	##crawl recent matches of summoner to get summoners he has played with
	##add summoners to db
	@staticmethod
	def grab_peers(s):
		print "Grabbing peers of summoner: " + s.name
			
		## update date_scraped_peers
		s.date_scraped_peers = datetime.datetime.utcnow()
		s.save()
		
		recent_matches_data = LeagueClient.get_recent_matches_data(s.league_id)
		peer_ids = Processor.extract_peers_ids(recent_matches_data)
		league_summoner_data = LeagueClient.get_summoner_data_all(peer_ids)
		Processor.populate_summoner_db(league_summoner_data)	

	##given summoner league data, add all new summoners to db
	@staticmethod
	def populate_summoner_db(data):
		for key in data:
			value = data[str(key)]
			name = value[0]["entries"][0]["playerOrTeamName"]
			league_id = key
			division = value[0]["entries"][0]["division"]
			tier = value[0]["tier"]
			##only grab diamond+ players
			if tier_converter[tier] <= 3:
				s_model = Summoner.get_summoner(name, league_id, division, tier)
				s_model.save()
	
	## grab peers of all challangers
	@staticmethod
	def grab_peers_challenger():
		print "Adding all peers of challengers to db"
		with DbClient() as db_client:
			cursor = db_client.get_summoners_on_tier("CHALLENGER")
			for o in cursor:
				s = Summoner.from_object(o)
				if check_time_diff(s.date_scraped_peers):
					Processor.grab_peers(s)

## return true if never scraped or scraped really long time ago (true allows new scrape)
def check_time_diff(dt_past):	
	if dt_past == None:
		##means summoner never got scraped
		return True
	else:
		time_elapsed = datetime.datetime.utcnow() - dt_past
		if time_elapsed.days > SCRAPE_RESET_DAYS:
			return True
		else:
			##TODO make a global request staggerer
			##sleep to prevent too many request
			time.sleep(5)
			return False



