## Summoner: id, name, league_id tier, division, date_scraped_peers 

from db_client import DbClient

## dict converts string to corresponding value so comparisons can be made
tier_converter = {
		"CHALLENGER" : 1,
		"MASTER" : 2,
		"DIAMOND" : 3,
		"PLATINUM" : 4,
		"GOLD" : 5,
		"SILVER" : 6,
		"BRONZE" : 7,
		"UNRANKED" : 8}

class Summoner:
	def __init__(self, name, league_id, tier, division, date_scraped_peers = None, id = None):
		self.id = id
		self.name = name
		self.league_id = league_id
		self.tier = tier
		self.division = division
		self.date_scraped_peers = None

	@classmethod
	def from_object(cls, o):
		id = o["_id"]
		name = o["name"]
		league_id = o["league_id"] 
		tier = o["tier"]
		division = o["division"]
		date_scraped_peers = o["date_scraped_peers"]
		
		return cls(name, league_id, tier, division, date_scraped_peers, id)
	
	## if summoner already exists in db return it, otherwise return new summoner object
	@classmethod
	def get_summoner(cls, name, league_id, tier, division):
		with DbClient() as db_client:
			cursor = db_client.find_summoner(league_id)
		
		##if doesn't exist in db
		if cursor.count() == 0:
			return cls(name, league_id, tier, division)
		else:
			##create model from summoner data in db
			assert (cursor.count() >= 1), "Error constructing Summoner model from cursor. Cursor is empty."
			summoner = cls.from_object(cursor[0])
			##update model attributes in case they changed
			summoner.name = name
			summoner.league_id = league_id
			summoner.tier = tier
			summoner.division = division
			return summoner

	def save(self):
		with DbClient() as db_client:
			##if already in db
			if self.id != None:
				db_client.update_summoner(self.id, self.name, self.tier, self.division, self.date_scraped_peers)
			else:
				self.id = db_client.create_summoner(self.name, self.league_id, self.tier, self.division, self.date_scraped_peers)
				
	
		
