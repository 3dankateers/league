## pair: id, champ1, champ2, type, winrate, winrate_sample_size, date_created
## looks for winrates among pairs of champions from oppositeor same teams(type)
from db_client import DbClient

class Pair:
	def __init__(self, champs, type, winrate = None, winrate_sample_size = None, id = None):
		self.id = id
		self.champ1 = champ1
		self.champ2 = champ2
		self.type = type
		self.winrate = winrate
		self.winrate_sample_size = winrate_sample_size
	
	@classmethod
	def from_dict(cls, d):
		id = d["_id"]
		champ1 = d["champ1"]
		champ2 = d["champ2"]
		type = d["type"]
		winrate = d["winrate"]
		winrate_sample_size = d["winrate_sample_size"]
		return cls(champ1, champ2, type, winrate, winrate_sample_size, id)

	
	## if pair already exists in db return it, otherwise return a new team
	@classmethod
	def get_pair(cls, champ1, champ2, type):
		with DbClient() as db_client:
			cursor = db_client.find_pair(champ1, champ2, type)
		
		##if doesn't exist in db
		if cursor.count() == 0:
			##match list will have to be populated somewhere else
			return cls(champ1, champ2, type)
		else:
			##create model from data in db
			assert (cursor.count() >= 1), "Error constructing Summoner model from cursor. Cursor is empty."
			pair = cls.from_dict(cursor[0])
			return pair
	
	def save(self):
		with DbClient() as db_client:	
			cursor = db_client.find_pair(self.id)
			##if already in db
			if cursor.count() > 0:
				db_client.update_pair(self.id, self.winrate, self.winrate_sample_size)
			else:
				self.id = db_client.create_pair(self.id, self.champ1, self.champ2, self.type, self.winrate, self.winrate_sample_size)
