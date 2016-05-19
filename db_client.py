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
		try:		
			print "Created summoner: " + name.encode(encoding='UTF-8',errors='replace')
		except:
			pass
	
	
	def create_team(self, summoners, matches, date_created):
		record = self.db.teams.insert_one({
				"summoners" : summoners,
				"matches" : matches,
				"date_created" : date_created
			})
		print "Created new team with ", str(len(matches)), " matches."
		return record.inserted_id

	def create_champ(self, id, name, winrate, winrate_sample_size):
		record = self.db.champs.insert_one({
				"_id" : id,
				"name" : name,
				"winrate" : winrate,
				"winrate_sample_size" : winrate_sample_size
			})
		print "created champ"

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
		try:		
			print "Updated summoner: " + name.encode(encoding='UTF-8',errors='replace')
		except:
			pass

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
	def update_champ(self, id, name, winrate, winrate_sample_size):
		self.db.champs.update_one(
				{"_id" : id},{
					"$set": {
						"winrate" : winrate,
						"winrate_sample_size" : winrate_sample_size
						}
				})
		print "Updated champ" 
	
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

	
	## find champ and return it based on id
	def find_champ(self, id):
		cursor = self.db.champs.find({"_id" : id})
		return cursor

	def find_champ_by_name(self, name):
		cursor = self.db.champs.find({"name" : name})
		return cursor

	def find_all_champs(self):
		cursor = self.db.champs.find()
		return cursor

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

