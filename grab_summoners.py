import json;
import urllib2

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


def parse_data(data):
	summoners = data["entries"]
	for s in summoners:
		print s

def main():
	data = get_challanger_data()
	parse_data(data)

main()
