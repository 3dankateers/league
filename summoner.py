## Summoner: id, name, league_id tier, division 

import db_client

class Summoner:
	def __init__(name, league_id, tier, division, id = None):
		self.id = id
		self.name = name
		self.league_id = league_id
		self.tier = tier
		self.division = divison

	@classmethod
	def from_cursor(cls, c):
		assert (c.count() == 1), "Error constructing Summoner model from cursor. Cursor is empty or contains multiple objects"
		id = c[0]["_id"]
		name = c[0]["name"]
		league_id = c[0]["league_id"] 
		tier = c[0]["tier"]
		division = c[0]["division"]
		return cls(name, league_id, tier, division, id)
	
	## if summoner already exists in db return it, otherwise return new summoner object
	@classmethod
	def get_summoner(name, league_id, tier, division):
		with DbClient() as db_client:
			cursor = db_client.find_summoner(league_id)
			##if doesn't exist in db
			if cursor.count() == 0:
				return cls(name, league_id, tier, divison)
			else:
				##create model from summoner data in db
				summoner = cls.from_cursor(cursor)
				##update model attributes in case they changed
				summoner.name = name
				summoner.league_id = league_id
				summoner.tier = tier
				summoner.diviison = division
				return summoner

	def save(self):
		with DbClient() as db_client:
			##if already in db
			if self.id != None:
				db_client.update_summoner(self.id, self.name, self.tier, self.division)
			else:
				self.id = db_client.create_summoner(self.name, self.league_id, self.tier, self.division)
				
	
		
