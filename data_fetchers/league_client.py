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

API_KEY = "?api_key=RGAPI-701617e2-5a7b-460d-b196-4c444150b7e6" 
HTTPS_PART = "https://"
API_PART = ".api.riotgames.com/lol/"
CHALLENGER_LEAGUE = "league/v3/challengerleagues/"
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

