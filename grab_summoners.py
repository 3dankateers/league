import json;
import urllib2
from summoner import Summoner

API_KEY = "&api_key=eeff2e9b-5f33-4de0-af17-16b98a4c4b3e" 
CHALLANGER_API = "https://na.api.pvp.net/api/lol/na/v2.5/league/challenger?type=RANKED_SOLO_5x5"

def getJSONReply(URL):
	response = urllib2.urlopen(URL);
	html = response.read();
	data = json.loads(html);
	return data;

def get_challanger_data():
	url = CHALLANGER_API + API_KEY 
	data = getJSONReply(url)
	return data


def extract_summoners(data):
	summoners = data["entries"]
	for s in summoners:
		name = s["playerOrTeamName"]
		league_id = s["playerOrTeamId"]
		division = s["division"]
		tier = "CHALLENGER"
		s_model = Summoner.get_summoner(name, league_id, division, tier)
		s_model.save()

		
def main():
	data = get_challanger_data()
	extract_summoners(data)

main()
