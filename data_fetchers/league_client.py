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

API_KEY = "?api_key=RGAPI-701617e2-5a7b-460d-b196-4c444150b7e6" 
HTTPS_PART = "https://"
API_PART = ".api.riotgames.com/lol/"
CHALLENGER_LEAGUE = "league/v3/challengerleagues/"
MATCH_LISTS = "match/v3/matchlists/by-account/"
MATCHES = "match/v3/matches/"
SUMMONER = "summoner/v3/summoners/"
RANKED_SOLO = "by-queue/RANKED_SOLO_5x5"

WAIT_TIME = 1500

def retry_if_url_error(exception):
	return isinstance(exception, URLError)


class LeagueClient:

    last_request = None

    ##may sleep to delay consecutive requests and make sure there is at most 1 request every 1.5 seconds
    def stagger_response(self):
        print "stagger"
        if self.last_request == None:
            self.last_request = time.time()
        else:
            print "here"
            t_delta = time.time() - self.last_request
            if t_delta < WAIT_TIME:
                print "waiting"
                time.sleep((WAIT_TIME - t_delta)/1000)
                self.last_request = time.time()
    
     
    @retry(retry_on_exception=retry_if_url_error)
    def urlopen_with_retry(self, url):
        return urllib2.urlopen(url)
    

    def getJSONReply(self, url):
            #self.stagger_response()
            response = self.urlopen_with_retry(url)
            Rate_Limiter(response)
            html = response.read();
            data = json.loads(html);
            return data;

    ##returns array of summoners from challenger league
    def get_challengers(self, region):
        data = self.getJSONReply(HTTPS_PART + region + API_PART + CHALLENGER_LEAGUE + RANKED_SOLO + API_KEY)
        tier = data["tier"]
        for e in data["entries"]:
            summonerID = e["playerOrTeamId"]
            accountID = self.summonerID_to_accountID(region, summonerID)
            date_scraped_matches = datetime.datetime.now()
            summoner = Summoner(summonerID, accountID, tier, region, date_scraped_matches)
            print "save summoner", summonerID
            summoner.save()

    def summonerID_to_accountID(self, region, summonerID):
        print region
        print summonerID
	try:
            url = HTTPS_PART + region + API_PART + SUMMONER + str(summonerID) + API_KEY
            data = self.getJSONReply(url)
            summonerdata = data
            accountID = summonerdata["accountId"]
            ##time.sleep(1)
            return accountID
	except KeyError, e:
            dump_to_file(summonerdata)
            print summonerdata
            print "Keyerror " + str(e)
            return -1

    ##inserts into db recent matches of the summoner array passed in
    def get_matches(self, region, tier):
        summoners = Summoner.get_summoners(region, tier)
        gameIDs = []
        for s in summoners:
            data = self.getJSONReply(HTTPS_PART + region + API_PART + MATCH_LISTS + str(s.accountID) + API_KEY)
            for e in data["matches"]:
                gameIDs.append(e["gameId"])
            for gameID in gameIDs:
                match = self.gameID_to_match(region, tier, gameID)
                match.save()

    ##returns match object from gameid+region
    def gameID_to_match(self, region, tier, gameID):
        data = self.getJSONReply(HTTPS_PART + region + API_PART + MATCHES + str(gameID) + API_KEY)
        patch = data["gameVersion"]
        gameType = data["gameType"]
        duration = data["gameDuration"]
        date = data["gameCreation"]
        ##TODO: fix this later
        team1 = "SOLOQ"
        team2 = "SOLOQ"
        

        if data["teams"][0]["firstBlood"]:
            first_blood = 100
        else:
            first_blood = 200
        
        if data["teams"][0]["win"]:
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
        m = Match(gameID, team1, team2, champs1, champs2, first_blood, duration, win, gameType, region, patch, tier, date)
        return m 

        

#Rate limiter, pauses the program if a rate goes above the league rate
def Rate_Limiter(response):
    #Gets data from league API headers, contains limit and how much youve used
    curAppCount = response.info().getheader('X-App-Rate-Limit-Count')
    curAppLimit = response.info().getheader('X-App-Rate-Limit')
    x = curAppCount.split(',')
    RequestsPerSecond = x[1].split(':')
    RequestsPerMinute = x[0].split(':')
    x = curAppLimit.split(',')
    MaxRequestsPerSecond = x[1].split(':')
    MaxRequestsPerMinute = x[0].split(':')

    if(int(RequestsPerMinute[0])>(int(MaxRequestsPerMinute[0])-2)):
        print "Rate too high, pausing for 30 secs"
        time.sleep(30)

    if(int(RequestsPerSecond[0])>(int(MaxRequestsPerSecond[0])-2)):
        print "Rate too high, pausing for 5 secs"
        time.sleep(5)

