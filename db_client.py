################################################################################################
## mondodb api
## db: league
##
## collections: summoners, matches
## Summoner: id, name, tier, division, region, date_scraped_peers, date_scraped_matches
## Match : id, team1, team2, champs1, champs2, duration, win, gametype, region, patch, tier, date
## Team : id, summoners, matches, date_created 
## Champ: id, name, winrate 
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

	## add new summoner to db 
	def create_summoner(self, id, name, tier, division, region, date_scraped_peers = None, date_scraped_matches = None):
		record = self.db.summoners.insert_one({
			"_id" : id,
			"name" : name,
			"tier" : tier,
			"division" : division,
			"region" : region,
			"date_scraped_peers" : date_scraped_peers,
			"date_scraped_matches" : date_scraped_matches
			})
		print "Created summoner: " + name.decode(encoding='UTF-8',errors='ignore')
	
	## add new match to db 
	def create_match(self, id, team1, team2, champs1, champs2, duration, win, gametype, region, patch, tier, date):	
		record = self.db.matches.insert_one({
			"_id" : id,
			"team1" : team1,
			"team2" : team2,
			"champs1" : champs1,
			"champs2" : champs2,
			"duration" : duration,
			"win" : win,
			"gametype" : gametype,
			"region" : region,
			"patch" : patch,
			"tier" : tier,
			"date" : date
			})
		print "Created match"
	
	def create_team(self, summoners, matches, date_created):
		record = self.db.teams.insert_one({
				"summoners" : summoners,
				"matches" : matches,
				"date_created" : date_created
			})
		print "Created new team with ", str(len(matches)), " matches."

	def create_champ(self, id, name, winrate):
		record = self.db.champs.insert_one({
				"_id" : id,
				"name" : name,
				"winrate" : winrate
			})
		print "created champ"

	## update existing summoner with new values passed in
	def update_summoner(self, id, name, tier, division, region, date_scraped_peers, date_scraped_matches):
		self.db.summoners.update_one(
				{"_id" : id},{
					"$set": {
						"name" : name,
						"tier" : tier,
						"division" : division,
						"region" : region,
						"date_scraped_peers" : date_scraped_peers,
						"date_scraped_matches" : date_scraped_matches
						}
				})
		print "Updated summoner: " + name.encode(encoding='UTF-8',errors='replace')

	## update existing team with new values passed in
	def update_team(self, id, matches):
		self.db.teams.update_one(
				{"_id" : id},{
					"$set": {
						"matches" : matches
						}
				})
		print "Updated team" 

	## update existing champ with new values passed in
	def update_team(self, id, name, winrate):
		self.db.champs.update_one(
				{"_id" : id},{
					"$set": {
						"winrate" : winrate
						}
				})
		print "Updated champ" 
	
	##mostly for testing
	##return first summoner found
	def get_one_summoner(self):
		cursor = self.db.summoners.find()
		if cursor.count() > 0:
			return cursor
		else:
			print "Summoner collection is empty"
			return None

	## return cursor to all summoners of the given tier
	def get_summoners_on_tier(self, t):
		cursor = self.db.summoners.find({"tier" : t})
		return cursor

	## find summoner and return it based on id
	def find_summoner(self, id):
		cursor = self.db.summoners.find({"_id" : id})
		return cursor

	## find match and return it based on id
	def find_match(self, id):
		cursor = self.db.matches.find({"_id" : id})
		return cursor
	
	## find champ and return it based on id
	def find_champ(self, id):
		cursor = self.db.champs.find({"_id" : id})
		return cursor

	## return all matches
	def get_all_matches(self):
		cursor = self.db.matches.find()
		return cursor

	## find team and return it based on list of summoners
	def find_team(self, summoners):
		cursor = self.db.teams.find({"summoners" : summoners})
		return cursor

