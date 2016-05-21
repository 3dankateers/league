################################################################################################
## mondodb api
## db: league
##
## collections: summoners, matches, teams, champs, pairs
## Summoner: id, name, tier, division, region, date_scraped_peers, date_scraped_matches
## Match : id, team1, team2, champs1, champs2, duration, win, gametype, region, patch, tier, date
## Team : id, summoners, matches, date_created 
## Champ: id, name, winrate, winrate_sample_size
## pair: id, champ1, champ2, type, winrate, winrate_sample_size, date_created
#################################################################################################

from pymongo import MongoClient

class DbClient:
	##MONGO_USERNAME = 'root'
	##MONGO_PASSWORD = 'm6E7K1GLwcz58q'

	def __init__(self):
		self.client = MongoClient("mongodb://localhost:27017/")
		self.db = self.client.league
		##self.db.authenticate(self.MONGO_USERNAME, self.MONGO_PASSWORD, source='admin')
	
	def __enter__(self):
		return self
	
	def __exit__(self, exc_type, exc_value, tb):
		self.client.close()

