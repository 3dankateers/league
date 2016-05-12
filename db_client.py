#####################################################################
## mondodb api
## db: league
##
## collection: summoners
## Summoner: id, name, tier, division, league_id 
#####################################################################

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

	## add new summoner to db and return its id
	def create_summoner(self, name, league_id, tier, division):
		record = self.db.summoners.insert_one({
			"name" : name,
			"league_id" : league_id,
			"tier" : tier,
			"division" : division
			})
		return record.inserted_id
	
	## update existing summoner with new values passed in
	def update_summoner(self, id, name, tier, division):
		self.db.summoners.update_one(
				{"_id" : id},{
					"$set": {
						"name" : name,
						"tier" : tier,
						"division" : division}
				})

	##mostly for testing
	##return first summoner found
	def get_one_summoner(self):
		cursor = self.db.summoners.find()
		if cursor.count() > 0:
			return cursor
		else:
			print "Summoner collection is empty"
			return None

	## find summoner and return it based on league_id
	def find_summoner(self, league_id):
		cursor = self.db.summoners.find({"league_id" : league_id})
		return cursor


