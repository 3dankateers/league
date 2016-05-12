########################################################################
## pulls data from league api
########################################################################


import json;
import urllib2
from summoner import Summoner
from db_client import DbClient

API_KEY = "api_key=eeff2e9b-5f33-4de0-af17-16b98a4c4b3e" 
CHALLANGER_ENDPOINT = "https://na.api.pvp.net/api/lol/na/v2.5/league/challenger?type=RANKED_SOLO_5x5"
GAME_ENDPOINT = "https://na.api.pvp.net/api/lol/na/v1.3/game/by-summoner/"	

##https://na.api.pvp.net/api/lol/na/v1.3/game/by-summoner/34287847/recent?api_key=eeff2e9b-5f33-4de0-af17-16b98a4c4b3e

class LeagueClient:
	
	@staticmethod
	def getJSONReply(URL):
		response = urllib2.urlopen(URL);
		html = response.read();
		data = json.loads(html);
		return data;

	@staticmethod
	def get_challanger_data():
		url = CHALLANGER_ENDPOINT + "&" + API_KEY 
		data = LeagueClient.getJSONReply(url)
		return data
	
	##return recent match data given a summoner id
	@staticmethod
	def get_recent_matches_data(s_id):
		url = GAME_ENDPOINT + str(s_id) + "/recent?" + API_KEY
		print url
		data = LeagueClient.getJSONReply(url)
		return data

	@staticmethod
	def extract_challangers(data):
		summoners = data["entries"]
		for s in summoners:
			name = s["playerOrTeamName"]
			league_id = s["playerOrTeamId"]
			division = s["division"]
			tier = "CHALLENGER"
			s_model = Summoner.get_summoner(name, league_id, division, tier)
			s_model.save()
	
	##given recent match data, return list of peers ids
	@staticmethod
	def extract_peers_ids(data):
		peer_ids = []
		games = data["games"]
		for g in games:
			peers = g["fellowPlayers"]
			for p in peers:
				s_id = p["summonerId"]
				peer_ids.append(s_id)
		return peer_ids

	##crawl recent matches of summoner to get summoners he has played with
	## add summoners to db
	@staticmethod
	def grab_peers(s):
		data = LeagueClient.get_recent_matches_data(s.league_id)
		peer_ids = LeagueClient.extract_peers_ids(data)
		print peer_ids



