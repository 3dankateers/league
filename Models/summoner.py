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
		with DbClient() as db_client:
			cursor = db_client.find_summoner(id)
		
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
		with DbClient() as db_client:	
			cursor = db_client.find_summoner(self.id)
			##if already in db
			if cursor.count() > 0:
				db_client.update_summoner(self.id, self.name, self.tier, self.division, self.region, self.date_scraped_peers, self.date_scraped_matches)
			else:
				db_client.create_summoner(self.id, self.name, self.tier, self.division, self.region, self.date_scraped_peers, self.date_scraped_matches)
				
	
		
