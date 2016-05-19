## pair: id, champ1, champ2, type, winrate, winrate_sample_size, date_created
## looks for winrates among pairs of champions from oppositeor same teams(type)
from db_client import DbClient

class Pair:
	def __init__(self, champ1, champ2, type, winrate = None, winrate_sample_size = None, id = None):

		## pair ignores order of champ1/champ2 passed in
		self.id = Pair.calc_id(champ1, champ2, type)

		self.pair_tuple = Pair.calc_pair_tuple(champ1, champ2)
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
				"_id" : self.id,
				"champ1" : self.champ1,
				"champ2" : self.champ2,
				"type" : self.type,
				"winrate" : self.winrate,
				"winrate_sample_size" : self.winrate_sample_size}
		return d
	
	## calculates unique id given champ1, champ2, type
	@staticmethod
	def calc_id(champ1, champ2, type):
		tup = Pair.calc_pair_tuple(champ1, champ2)
		id = int(str(tup[0])+ "0000" + str(tup[1]))
		if type == "enemy":
			id *= -1
		return id

	@staticmethod
	def calc_pair_tuple(c1,c2):
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
	def find_pair(db_client, id):
		cursor = db_client.db.pairs.find({
			"_id" : id})
		return cursor
