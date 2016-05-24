########################################################################
## pulls data from league api
########################################################################


import json;
import urllib2
from urllib2 import URLError
import datetime
import time
from retrying import retry

API_KEY = "api_key=eeff2e9b-5f33-4de0-af17-16b98a4c4b3e" 
HTTPS = "https://"
GLOBAL = "global"
API_PART =  ".api.pvp.net/api/lol/"
CHALLENGER_ENDPOINT = "/v2.5/league/challenger?type=RANKED_SOLO_5x5"
MASTER_ENDPOINT = "/v2.5/league/master?type=RANKED_SOLO_5x5"
GAME_ENDPOINT = "/v1.3/game/by-summoner/"	
LEAGUE_ENDPOINT = "/v2.5/league/by-summoner/"
STATIC_ENDPOINT = ".api.pvp.net/api/lol/static-data/na/v1.2/champion"

WAIT_TIME = 1500

def retry_if_url_error(exception):
	return isinstance(exception, URLError)


class LeagueClient:

	def __init__(self, region):
		self.region = region
		self.last_request = time.time()

	##may sleep to delay consecutive requests and make sure there is at most 1 request every 1.5 seconds
	def stagger_response(self):
		if self.last_request == None:
			self.last_request = time.time()
		else:
			t_delta = time.time() - self.last_request
			if t_delta < WAIT_TIME:
				print "waiting"
				time.sleep((WAIT_TIME - t_delta)/1000)
				self.last_request = time.time()
	
	
	@retry(retry_on_exception=retry_if_url_error)
	def urlopen_with_retry(self, url):
		return urllib2.urlopen(url)
	

	def getJSONReply(self, url):
		print url
		self.stagger_response()
		response = self.urlopen_with_retry(url)
		html = response.read();
		data = json.loads(html);
		return data;

	##get all champions
	def get_champ_data(self):
		url = HTTPS + GLOBAL +  STATIC_ENDPOINT + "?" + API_KEY 
		data = self.getJSONReply(url)
		return data

	##get challenger summoners
	def get_challanger_data(self):
		url = HTTPS + self.region + API_PART + self.region + CHALLENGER_ENDPOINT + "&" + API_KEY 
		data = self.getJSONReply(url)
		return data
	
	##get challenger summoners
	def get_master_data(self):
		url = HTTPS + self.region + API_PART + self.region + MASTER_ENDPOINT + "&" + API_KEY 
		data = self.getJSONReply(url)
		return data
	
	##return recent match data given a summoner id
	def get_recent_matches_data(self, s_id):
		url = HTTPS + self.region + API_PART + self.region + GAME_ENDPOINT + str(s_id) + "/recent?" + API_KEY
		data = self.getJSONReply(url)
		return data

	##return summoner data for a list of summoner ids
	def get_summoner_data(self, s_ids):
		assert s_ids > 1, "get_summoner_data called with empty s_ids"
		url = HTTPS + self.region + API_PART + self.region + LEAGUE_ENDPOINT
		url += str(s_ids[0])	
		for s_id in s_ids:
			url += ","
			url += str(s_id)
		url += "/entry?"
		url += API_KEY
		data = self.getJSONReply(url)
		return data

	##wrapper that limits each api call by 10 s_ids 	
	def get_summoner_data_all(self, s_ids):
		lower = 0
		upper = 9
		final_data = {}
		while upper < len(s_ids):
			data = self.get_summoner_data(s_ids[lower:upper])
			final_data.update(data)
			lower = upper + 1
			upper = min((upper+10), len(s_ids))
		return final_data



