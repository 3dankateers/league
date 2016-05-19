## Summoner: id, name, tier, division, region, date_scraped_peers, date_scraped_matches

from db_client import DbClient

class Summoner:
	def __init__(self, id, name, tier, division, region, date_scraped_peers = None, date_scraped_matches = None):
		self.name = name
		self.id = id
		self.tier = tier
		self.division = division
		self.region = region
		self.date_scraped_peers = date_scraped_peers
		self.date_scraped_matches = date_scraped_matches

	@classmethod
	def from_dict(cls, d):
		id = d["_id"]
		name = d["name"]
		tier = d["tier"]
		division = d["division"]
		region = d["region"]
		date_scraped_peers = d["date_scraped_peers"]
		date_scraped_matches = d["date_scraped_matches"]
		
		return cls(id, name, tier, division, region, date_scraped_peers, date_scraped_matches)
	
	## if summoner already exists in db return it, otherwise return new summoner object
	@classmethod
	def get_summoner(cls, id, name, tier, division, region):
		cursor = Summoner.find_summoner(id)
		
		##if doesn't exist in db
		if cursor.count() == 0:
			return cls(id, name, tier, division, region)
		else:
			##create model from summoner data in db
			assert (cursor.count() >= 1), "Error constructing Summoner model from cursor. Cursor is empty."
			summoner = cls.from_dict(cursor[0])
			
			##update model attributes in case they changed
			summoner.name = name
			summoner.tier = tier
			summoner.division = division
			summoner.region = region
			return summoner

	def save(self):
		cursor = Summoner.find_summoner(self.id)
		##if already in db
		if cursor.count() > 0:
			self.update_summoner()
		else:
			self.create_summoner()
				
	## add new summoner to db 
	def create_summoner(self):
		with DbClient() as db_client:
			record = db_client.db.summoners.insert_one({
				"_id" : self.id,
				"name" : self.name,
				"tier" : self.tier,
				"division" : self.division,
				"region" : self.region,
				"date_scraped_peers" : self.date_scraped_peers,
				"date_scraped_matches" : self.date_scraped_matches
				})
			try:		
				print "Created summoner: " + self.name.encode(encoding='UTF-8',errors='replace')
			except:
				pass
		
	## update existing summoner with new values 
	def update_summoner(self):
		with DbClient() as db_client:
			db_client.db.summoners.update_one(
					{"_id" : self.id},{
						"$set": {
							"name" : self.name,
							"tier" : self.tier,
							"division" : self.division,
							"region" : self.region,
							"date_scraped_peers" : self.date_scraped_peers,
							"date_scraped_matches" : self.date_scraped_matches
							}
					})
			try:		
				print "Updated summoner: " + self.name.encode(encoding='UTF-8',errors='replace')
			except:
				pass

	##mostly for testing
	##return first summoner found
	@staticmethod
	def get_one_summoner():
		with DbClient() as db_client:
			cursor = db_client.db.summoners.find()
			if cursor.count() > 0:
				return cursor
			else:
				print "Summoner collection is empty"
				return None
	
	## return cursor to all summoners of the given tier
	@staticmethod
	def get_summoners_on_tier(t):
		with DbClient() as db_client:
			cursor = db_client.db.summoners.find({"tier" : t})
			return cursor
	
	
	## find summoner and return it based on id
	@staticmethod
	def find_summoner(id):
		with DbClient() as db_client:
			cursor = db_client.db.summoners.find({"_id" : id})
			return cursor
