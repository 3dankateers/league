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
		cursor = Champ.find_champ(id)
		
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
		cursor = Champ.find_champ(self.id)
		##if already in db
		if cursor.count() > 0:
			self.update_champ()
		else:
			self.create_champ()

	
	def create_champ(self):
		with DbClient() as db_client():
			record = db_client.db.champs.insert_one({
					"_id" : self.id,
					"name" : self.name,
					"winrate" : self.winrate,
					"winrate_sample_size" : self.winrate_sample_size
				})
			print "created champ"
	
	## update existing champ with new values passed in
	def update_champ(self):
		with DbClient() as db_client():
			db_client.db.champs.update_one(
					{"_id" : self.id},{
						"$set": {
							"winrate" : self.winrate,
							"winrate_sample_size" : self.winrate_sample_size
							}
					})
			print "Updated champ" 
	
	## find champ and return it based on id
	@staticmethod
	def find_champ(id):
		with DbClient() as db_client:
			cursor = db_client.db.champs.find({"_id" : id})
			return cursor

	@staticmethod
	def find_champ_by_name(name):
		with DbClient() as db_client:
			cursor = db_client.db.champs.find({"name" : name})
			return cursor

	@staticmethod
	def find_all_champs():
		with DbClient() as db_client:
			cursor = db_client.db.champs.find()
			return cursor
