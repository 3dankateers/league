########################################################################
## pulls data from league api
########################################################################


import json;
import urllib2

API_KEY = "api_key=eeff2e9b-5f33-4de0-af17-16b98a4c4b3e" 
CHALLANGER_ENDPOINT = "https://na.api.pvp.net/api/lol/na/v2.5/league/challenger?type=RANKED_SOLO_5x5"
GAME_ENDPOINT = "https://na.api.pvp.net/api/lol/na/v1.3/game/by-summoner/"	
LEAGUE_ENDPOINT = "https://na.api.pvp.net/api/lol/na/v2.5/league/by-summoner/"

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
		data = LeagueClient.getJSONReply(url)
		return data

	##return summoner data for a list of summoner ids
	@staticmethod
	def get_summoner_data(s_ids):
		assert s_ids > 1, "get_summoner_data called with empty s_ids"
		url = LEAGUE_ENDPOINT
		url += str(s_ids[0])	
		for s_id in s_ids:
			url += ","
			url += str(s_id)
		url += "/entry?"
		url += API_KEY
		data = LeagueClient.getJSONReply(url)
		return data

	##wrapper that limits each api call by 10 s_ids 	
	@staticmethod
	def get_summoner_data_all(s_ids):
		lower = 0
		upper = 9
		final_data = {}
		while upper < len(s_ids):
			data = LeagueClient.get_summoner_data(s_ids[lower:upper])
			final_data.update(data)
			lower = upper + 1
			upper = min((upper+10), len(s_ids))
		return final_data



