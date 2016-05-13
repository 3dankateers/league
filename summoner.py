## Summoner: id, name, league_id tier, division, region, date_scraped_peers, date_scraped_matches

from db_client import DbClient

class Summoner:
	def __init__(self, name, league_id, tier, division, region, date_scraped_peers = None, date_scraped_matches = None, id = None):
		self.id = id
		self.name = name
		self.league_id = league_id
		self.tier = tier
		self.division = division
		self.region = region
		self.date_scraped_peers = date_scraped_peers
		self.date_scraped_matches = date_scraped_matches

	@classmethod
	def from_object(cls, o):
		id = o["_id"]
		name = o["name"]
		league_id = o["league_id"] 
		tier = o["tier"]
		division = o["division"]
		region = o["region"]
		date_scraped_peers = o["date_scraped_peers"]
		date_scraped_matches = o["date_scraped_matches"]
		
		return cls(name, league_id, tier, division, region, date_scraped_peers, date_scraped_matches, id)
	
	## if summoner already exists in db return it, otherwise return new summoner object
	@classmethod
	def get_summoner(cls, name, league_id, tier, division, region):
		with DbClient() as db_client:
			cursor = db_client.find_summoner(league_id)
		
		##if doesn't exist in db
		if cursor.count() == 0:
			return cls(name, league_id, tier, division, region)
		else:
			##create model from summoner data in db
			assert (cursor.count() >= 1), "Error constructing Summoner model from cursor. Cursor is empty."
			summoner = cls.from_object(cursor[0])
			
			##update model attributes in case they changed
			summoner.name = name
			summoner.league_id = league_id
			summoner.tier = tier
			summoner.division = division
			summoner.region = region
			return summoner

	def save(self):
		with DbClient() as db_client:
			##if already in db
			if self.id != None:
				db_client.update_summoner(self.id, self.name, self.tier, self.division, self.region, self.date_scraped_peers, self.date_scraped_matches)
			else:
				self.id = db_client.create_summoner(self.name, self.league_id, self.tier, self.division, self.region, self.date_scraped_peers, self.date_scraped_matches)
				
	
		
