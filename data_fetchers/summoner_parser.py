########################################################################
## parses data from league_client
## inserts new data into db
########################################################################

import datetime
import time
from summoner import Summoner
from db_client import DbClient
from league_client import LeagueClient
from misc_helper import MiscHelper


class SummonerParser:
	
	##add all summoners to db
	@staticmethod
	def add_summoners_to_db(lc, tier):
		print "Adding all summoners to db..."
		if tier == "CHALLENGER":
			data = lc.get_challanger_data()
		else:
			data = lc.get_master_data()
		SummonerParser.populate_summoners(lc, tier, data)


	## populate db with all challangers given data
	@staticmethod
	def populate_summoners(lc, t, data):
		summoners = data["entries"]
		for s in summoners:
			name = s["playerOrTeamName"].encode(encoding='UTF-8',errors='replace')
			id = s["playerOrTeamId"]
			division = s["division"]
			region = lc.region
			tier = t
			s_model = Summoner.get_summoner(id, name, tier, division, region)
			s_model.save()
	
	##given recent match data, return list of peers ids
	@staticmethod
	def extract_peers_ids(data):
		peer_ids = []
		games = data["games"]
		for g in games:

		##only care about ranked 5v5 games
			if (MiscHelper.check_game_type(g)):
				peers = g["fellowPlayers"]
				for p in peers:
					s_id = p["summonerId"]
					peer_ids.append(s_id)
		return peer_ids

	##crawl recent matches of summoner to get summoners he has played with
	##add summoners to db
	@staticmethod
	def grab_peers(lc, s):
		print "Grabbing peers of summoner: " + s.name.encode(encoding='UTF-8',errors='replace')

			
		## update date_scraped_peers
		s.date_scraped_peers = datetime.datetime.utcnow()
		s.save()
		
		recent_matches_data = lc.get_recent_matches_data(s.id)
		peer_ids = SummonerParser.extract_peers_ids(recent_matches_data)
		league_summoner_data = lc.get_summoner_data_all(peer_ids)
		SummonerParser.populate_summoner_db(lc, league_summoner_data)	

	##given summoner league data, add all new summoners to db
	@staticmethod
	def populate_summoner_db(lc, data):
		for key in data:
			value = data[str(key)]
			name = value[0]["entries"][0]["playerOrTeamName"].encode(encoding='UTF-8',errors='replace')
			id = key
			tier = value[0]["tier"]
			division = value[0]["entries"][0]["division"]
			region = lc.region
			##only grab diamond+ players
			if MiscHelper.tier_converter[tier] <= 3:
				s_model = Summoner.get_summoner(id, name, tier, division, region)
				s_model.save()
	
	## grab peers of all challangers
	@staticmethod
	def grab_peers_challenger(lc):
		print "Adding all peers of challengers to db"
		cursor = Summoner.get_summoners_on_tier("CHALLENGER")
		for d in cursor:
			s = Summoner.from_dict(d)
			if MiscHelper.check_time_diff(s.date_scraped_peers):
				SummonerParser.grab_peers(lc, s)



