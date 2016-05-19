## pair: id, champ1, champ2, type, winrate, winrate_sample_size, date_created
## looks for winrates among pairs of champions from oppositeor same teams(type)
from db_client import DbClient

class Pair:
	def __init__(self, champ1, champ2, type, winrate = None, winrate_sample_size = None, id = None):
		self.id = id

		## pair ignores order of champ1/champ2 passed in

		self.pair_tuple = Pair.get_pair_tuple(champ1, champ2)
		self.champ1 = self.pair_tuple[0]
		self.champ2 = self.pair_tuple[1]
		
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

	def to_dict(self):
		d = { 
				"champ1" : self.champ1,
				"champ2" : self.champ2,
				"type" : self.type,
				"winrate" : self.winrate,
				"winrate_sample_size" : self.winrate_sample_size}
		return d

	## if pair already exists in db return it, otherwise return a new team
	@classmethod
	def get_pair(cls, champ1, champ2, type):
		sorted_champs = [champ1, champ2]
		sorted_champs.sort()
		with DbClient() as db_client:
			cursor = Pair.find_pair(sorted_champs[0], sorted_champs[1], type)
		
		##if doesn't exist in db
		if cursor.count() == 0:
			##match list will have to be populated somewhere else
			return cls(champ1, champ2, type)
		else:
			##create model from data in db
			assert (cursor.count() >= 1), "Error constructing Summoner model from cursor. Cursor is empty."
			pair = cls.from_dict(cursor[0])
			return pair

	@staticmethod
	def get_pair_tuple(c1,c2):
		sorted_champs = [c1, c2]
		sorted_champs.sort()
		pair_tuple = (sorted_champs[0], sorted_champs[1])
		return pair_tuple
	
	def save(self):
		##if already in db
		if self.id != None:
			self.update_pair()
		else:
			self.id = self.create_pair()
	
	def create_pair(self):
		with DbClient() as db_client:
			record = db_client.db.pairs.insert_one({
					"champ1" : self.champ1,
					"champ2" : self.champ2,
					"type" : self.type,
					"winrate" : self.winrate,
					"winrate_sample_size" : self.winrate_sample_size
				})
			print "created pair"
			return record.inserted_id
	
	## update existing pair with new values 
	def update_pair(self):
		with DbClient() as db_client:
			db_client.db.pairs.update_one(
					{"_id" : self.id},{
						"$set": {
							"winrate" : self.winrate,
							"winrate_sample_size" : self.winrate_sample_size
							}
					})
			print "Updated pair." 

	##insert multiple documents
	@staticmethod
	def insert_all(dicts):
		with DbClient() as db_client:
			db_client.db.pairs.insert(dicts)

	## delete all documents
	@staticmethod
	def drop_all():
		with DbClient() as db_client:
			db_client.db.pairs.drop()
	
	## find pair and return it based on champ1, champ2, and type
	@staticmethod
	def find_pair(champ1, champ2, type):
		with DbClient() as db_client:
			cursor = db_client.db.pairs.find({
				"champ1" : champ1,
				"champ2" : champ2,
				"type" : type})
			return cursor
