########################################################################
## pulls data from league api
########################################################################


import json;
import urllib2
from urllib2 import URLError
import datetime
import time
from retrying import retry
from summoner import Summoner
from match import Match
from champ import Champ
HTTPS_PART = "https://"
API_PART = ".api.riotgames.com/lol/"
CHALLENGER_LEAGUE = "league/v3/challengerleagues/"
MASTER_LEAGUE = "league/v3/masterleagues/"
MATCH_LISTS = "match/v3/matchlists/by-account/"

MATCHES = "match/v3/matches/"
CHAMPS = "static-data/v3/champions?locale=en_US&dataById=false"
SUMMONER = "summoner/v3/summoners/"
RANKED_SOLO = "by-queue/RANKED_SOLO_5x5"
RANKED_FLEX_SR = "by-queue/RANKED_FLEX_SR"

BEGINTIME_PART = "&beginTime="
ENDTIME_PART = "&endTime="
QUEUE_PART = "?queue="

WAIT_TIME = 1500

## retries to hit endpoint if the response is a URL ERROR. Max retries = 4 with 3 sec delay in between 
@retry(stop_max_attempt_number=4)
def urlopen_with_retry(url):
		print url
		return urllib2.urlopen(url)


class LeagueClient:

	last_request = None
	API_KEY = "api_key=" 

	def __init__(self):
		f  = open("./data_fetchers/apikey.txt", "r")
		key = f.readline()
		self.API_KEY += key
		
	## tries to return json data from url, retries if somethign goes wrong
				## if retries also fail, handle error on case by case basis and return -1
	def getJSONReply(self, url, rate_limit = True):
		try:
			response = urlopen_with_retry(url)
			if rate_limit:
				rate_limiter(response)
				html = response.read();
				data = json.loads(html);
				return data;
		except URLError, e:
			self.handle_url_error(url, e)
			return -1

				##handles all url errors on a case by case basis, add more cases here in the future
	def handle_url_error(self, url, e):
		print url
		print e.reason

		if e.reason == "Not Found":
			if CHALLENGER_LEAGUE in url:
				print "Can't find challengers"
			elif MATCH_LISTS in url:
				accountID = int(url.split("?")[0].split("/")[-1])## gets the number between the / and the first question mark. URL format is .../{AccountID}?...
				#Summoner.delete_summoner(accountID)
				#print "Cant grab data for accountID: " + str(accountID) + " , deleted it"
				print "Cant grab data for accountID: " + str(accountID)
			elif CHAMPS in url:
				print "Url Error on get champs"
			elif e.reason == "Forbidden":
				print "Probably forgot your API Key refresh"
			elif e.reason == "Too Many Requests":
				print "Too Many requests, pausing for 30 secs"
				time.sleep(30)

	
	def get_champs(self, region):
		data = self.getJSONReply(HTTPS_PART + region + API_PART + CHAMPS + "&" + self.API_KEY, rate_limit = False)
		if data == -1:
			return 
			for key in data["data"]:
				champID = data["data"][key]["id"]
				name = key
				c = Champ(champID, key)
				c.save()
		
	##inserts summoners from challenger league
	def get_challengers(self, region):
		data = self.getJSONReply(HTTPS_PART + region + API_PART + CHALLENGER_LEAGUE + RANKED_SOLO + "?" + self.API_KEY)
		if data == -1:
			return 
		else:
			tier = data["tier"]
			for e in data["entries"]:
				summonerID = e["playerOrTeamId"]
				accountID = self.summonerID_to_accountID(region, summonerID)
				if accountID == -1:
					continue 
				date_scraped_matches = datetime.datetime.now()
				summoner = Summoner(summonerID, accountID, tier, region, 420, date_scraped_matches)
				print "save summoner", summonerID
				summoner.save()

	def get_challengers_flexSR(self, region):
		data = self.getJSONReply(HTTPS_PART + region + API_PART + CHALLENGER_LEAGUE + RANKED_FLEX_SR + "?" + self.API_KEY)
		if data == -1:
									 return 
		else:
										tier = data["tier"]
										for e in data["entries"]:
												summonerID = e["playerOrTeamId"]
												accountID = self.summonerID_to_accountID(region, summonerID)
												if accountID == -1:
													 continue 
												date_scraped_matches = datetime.datetime.now()
												summoner = Summoner(summonerID, accountID, tier, region, 440, date_scraped_matches)
												print "save summoner", summonerID
												summoner.save()

	def get_masters_solo5x5(self, region):
		data = self.getJSONReply(HTTPS_PART + region + API_PART + MASTER_LEAGUE + RANKED_SOLO + "?" + self.API_KEY)
		if data == -1:
			return 
		else:
			tier = data["tier"]
			for e in data["entries"]:
				summonerID = e["playerOrTeamId"]
				accountID = self.summonerID_to_accountID(region, summonerID)
				if accountID == -1:
					continue 
				date_scraped_matches = datetime.datetime.now()
				summoner = Summoner(summonerID, accountID, tier, region, 420, date_scraped_matches)
				print "save summoner", summonerID
				summoner.save()

	def get_masters_flexSR(self, region):
		data = self.getJSONReply(HTTPS_PART + region + API_PART + MASTER_LEAGUE + RANKED_FLEX_SR + "?" + self.API_KEY)
		if data == -1:
			return 
		else:
			tier = data["tier"]
			for e in data["entries"]:
				summonerID = e["playerOrTeamId"]
				accountID = self.summonerID_to_accountID(region, summonerID)
				if accountID == -1:
					continue 
				date_scraped_matches = datetime.datetime.now()
				summoner = Summoner(summonerID, accountID, tier, region, 440, date_scraped_matches)
				print "save summoner", summonerID
				summoner.save()

	def summonerID_to_accountID(self, region, summonerID):
		print region
		print summonerID
		try:
			summonerdata = self.getJSONReply(HTTPS_PART + region + API_PART + SUMMONER + str(summonerID) + "?" + self.API_KEY)
			if(summonerdata != -1):
				accountID = summonerdata["accountId"]
				##time.sleep(1)
				return accountID
			else:
				print "Error hereeeeeeeeeeeeeeeeeeeeeeeeeeee"
				return -1
		except KeyError, e:
			dump_to_file(summonerdata)
			print summonerdata
			print "Keyerror " + str(e)
			return -1


	##inserts into db recent matches of the summoner array passed in
	## currently uses recent matches endpoint (if need be modify later to get older matches)
	## Added startTime and EndTime as a way to search for 
	## endTime - startTime have to be at most a week or else leagueapi tells you its too long ago
	## This should make it easier if we want to update games of players on a certain cycle probably
	## 	around the time it takes for a korean to grind 100 games (max query) which is probably about
	##	50 hours, so every 3 dayz should do the trick
	## 420 = solo 5x5 440 = flex 5x5

	def get_matches(self, region, tier, queue = 420, startTime = time.time()-1000000, endTime = time.time()-500000):

		if ((int(endTime) - int(startTime)) > 500000):
			startTime = endTime - 500000

		#league format of timestamp
		startTime *= 1000
		endTime *= 1000

		#set to int or else you get cancer and url dont like
		startTime = int(startTime)
		endTime = int(endTime)

		summoners = Summoner.get_summoners(region, tier, queue)
		gameIDs = []
		for s in summoners:
			data = self.getJSONReply(HTTPS_PART + region + API_PART + MATCH_LISTS + str(s.accountID) + QUEUE_PART + str(queue) + ENDTIME_PART + str(endTime) + BEGINTIME_PART + str(startTime) + "&" + self.API_KEY)
			if(data==-1):
				continue ## on url error, move on to next summoner
			else:
				for e in data["matches"]:
					gameIDs.append(e["gameId"])
				for gameID in gameIDs:
					match = self.gameID_to_match(region, tier, gameID)
					if match != None:
						match.save()

	##returns match object from gameid+region
	def gameID_to_match(self, region, tier, gameID):
		##return None if match already exists
		if Match.exists_match(gameID):
				return None
		data = self.getJSONReply(HTTPS_PART + region + API_PART + MATCHES + str(gameID) + "?" + self.API_KEY)
		if data == -1: ## if we got url error, return None which results in parent function move on to next match
			return None
			
		patch = data["gameVersion"]
		gameType = data["gameType"]
		queueId = data["queueId"]
		duration = data["gameDuration"]
		date = data["gameCreation"]
		##TODO: fix this later
		team1 = "SOLOQ"
		team2 = "SOLOQ"
		

		if data["teams"][0]["firstBlood"]:
			first_blood = 100
		else:
			first_blood = 200
		
		if data["teams"][0]["win"] == "Win":
			win = 100
		else:
			win = 200
		
		##get champion pick info
		champs1 = []
		champs2 = []
		for p in data["participants"]:
			if p["teamId"] == 100:
				champs1.append(p["championId"])
			else:
				champs2.append(p["championId"])
		m = Match(gameID, team1, team2, champs1, champs2, first_blood, duration, win, queueId, region, patch, tier, date)
		return m 

		

#Rate limiter, pauses the program if a rate goes above the league rate
def rate_limiter(response):
	if response == "Forbidden":
		print "You probably forgot to update your API key"

	else:
		#Gets data from league API headers, contains limit and how much youve used
		curAppCount = response.info().getheader('X-App-Rate-Limit-Count')
		curAppLimit = response.info().getheader('X-App-Rate-Limit')

		x = curAppCount.split(',')
		RequestsPerSecond = x[1].split(':')
		RequestsPerMinute = x[0].split(':')
		x = curAppLimit.split(',')
		MaxRequestsPerSecond = x[1].split(':')
		MaxRequestsPerMinute = x[0].split(':')

		if(int(RequestsPerMinute[0])>(int(MaxRequestsPerMinute[0])-5)):
			print "Rate too high, pausing for 20 secs"
			time.sleep(20)

		if(int(RequestsPerSecond[0])>(int(MaxRequestsPerSecond[0])-5)):
			print "Rate too high, pausing for 15 secs"
			time.sleep(20)


