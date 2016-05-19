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
	MONGO_USERNAME = 'root'
	MONGO_PASSWORD = 'm6E7K1GLwcz58q'

	def __init__(self):
		self.client = MongoClient("mongodb://54.191.167.105:27017")
		self.db = self.client.league
		self.db.authenticate(self.MONGO_USERNAME, self.MONGO_PASSWORD, source='admin')
	
	def __enter__(self):
		return self
	
	def __exit__(self, exc_type, exc_value, tb):
		self.client.close()

	def create_team(self, summoners, matches, date_created):
		record = self.db.teams.insert_one({
				"summoners" : summoners,
				"matches" : matches,
				"date_created" : date_created
			})
		print "Created new team with ", str(len(matches)), " matches."
		return record.inserted_id


	def create_pair(self, champ1, champ2, type, winrate, winrate_sample_size):
		record = self.db.pairs.insert_one({
				"champ1" : champ1,
				"champ2" : champ2,
				"type" : type,
				"winrate" : winrate,
				"winrate_sample_size" : winrate_sample_size
			})
		print "created pair"
		return record.inserted_id
	
	## update existing team with new values passed in
	def update_team(self, id, matches):
		self.db.teams.update_one(
				{"_id" : id},{
					"$set": {
						"matches" : matches
						}
				})
		print "Updated team" 

	
	## update existing pair with new values passed in
	def update_pair(self, id, winrate, winrate_sample_size):
		self.db.pairs.update_one(
				{"_id" : id},{
					"$set": {
						"winrate" : winrate,
						"winrate_sample_size" : winrate_sample_size
						}
				})
		print "Updated pair." 
	

	## find pair and return it based on champ1, champ2, and type
	def find_pair(self, champ1, champ2, type):
		cursor = self.db.pairs.find({
			"champ1" : champ1,
			"champ2" : champ2,
			"type" : type})
		return cursor
	

	## find team and return it based on list of summoners
	def find_team(self, summoners):
		cursor = self.db.teams.find({"summoners" : summoners})
		return cursor

