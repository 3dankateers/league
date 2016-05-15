## Champ: id, name, winrate, winrate_sample_size 

from db_client import DbClient

class Champ:
	def __init__(self, id, name, winrate = None, winrate_sample_size = None):
		self.id = id
		self.name = name
		self.winrate = winrate
		self.winrate_sample_size = winrate_sample_size

	@classmethod
	def from_dict(cls, d):
		id = d["_id"]
		name = d["name"]
		winrate = d["winrate"]
		winrate_sample_size = d["winrate_sample_size"]
		
		return cls(id, name, winrate, winrate_sample_size)

	
	## if team already exists in db return it, otherwise return a new team
	@classmethod
	def get_champ(cls, id, name):
		with DbClient() as db_client:
			cursor = db_client.find_champ(id)
		
		##if doesn't exist in db
		if cursor.count() == 0:
			##match list will have to be populated somewhere else
			return cls(id, name)
		else:
			##create model from champ data in db
			assert (cursor.count() >= 1), "Error constructing Summoner model from cursor. Cursor is empty."
			champ = cls.from_dict(cursor[0])
			return champ
	
	def save(self):
		with DbClient() as db_client:	
			cursor = db_client.find_champ(self.id)
			##if already in db
			if cursor.count() > 0:
				db_client.update_champ(self.id, self.name, self.winrate, self.winrate_sample_size)
			else:
				db_client.create_champ(self.id, self.name, self.winrate, self.winrate_sample_size)


