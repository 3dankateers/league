## pair: id, champ1, champ2, type, winrate, winrate_sample_size, date_created
## looks for winrates among pairs of champions from oppositeor same teams(type)
from db_client import DbClient

class Pair:
	def __init__(self, champ1, champ2, type, winrate = None, winrate_sample_size = None, id = None):
		self.id = id

		## pair ignores order of champ1/champ2 passed in
		sorted_champs = [champ1, champ2]
		sorted_champs.sort()

		self.champ1 = sorted_champs[0]
		self.champ2 = sorted_champs[1]
		self.pair_tuple = (self.champ1, self.champ2)
		
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
		sorted_champs = [champ1, champ2]
		sorted_champs.sort()
		with DbClient() as db_client:
			cursor = db_client.find_pair(sorted_champs[0], sorted_champs[1], type)
		
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
			##if already in db
			if self.id != None:
				db_client.update_pair(self.id, self.winrate, self.winrate_sample_size)
			else:
				self.id = db_client.create_pair(self.champ1, self.champ2, self.type, self.winrate, self.winrate_sample_size)
