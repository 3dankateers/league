## Champ: id, name, winrate 

from db_client import DbClient

class Champ:
	def __init__(self, id, name, winrate = None):
		self.id = id
		self.name = name
		self.winrate = winrate

	@classmethod
	def from_dict(cls, d):
		id = d["_id"]
		name = d["name"]
		winrate = d["winrate"]
		
		return cls(id, name, winrate)

	
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
			##create model from summoner data in db
			assert (cursor.count() >= 1), "Error constructing Summoner model from cursor. Cursor is empty."
			champ = cls.from_dict(cursor[0])
			return champ
