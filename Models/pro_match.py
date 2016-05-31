## pro_match : id, description, champs1, champs2, win, region, patch, date_created, is_test
import time
from db_client import DbClient

class ProMatch:
	def __init__(self, description, champs1, champs2, win, region, patch, date_created = int(round(time.time() * 1000)), id =None, is_test = False):
		self.id = id
		self.description = description
		self.champs1 = champs1
		self.champs2 = champs2
		self.win = win
		self.region = region
		self.patch = patch
		self.date_created = date_created
		self.is_test = is_test
	
	@classmethod
	def from_dict(cls, d):
		id = d["_id"]
		description = d["description"]
		champs1 = d["champs1"]
		champs2 = d["champs2"]
		win = d["win"]
		region = d["region"]
		patch = d["patch"]
		date_created = d["date_created"]
		is_test = d["is_test"]
		
		return cls(description, champs1, champs2, win, region, patch, date_created, id = id, is_test = is_test)
	
	## push match into database
	def save(self):
		self.id = self.create_pro_match()
	
	## find match and return it based on id
	@staticmethod
	def find_match(id):
		db_client = DbClient.get_client()
		cursor = db_client.league.pro_matches.find({"_id" : id})
		return cursor
	
	## return all matches
	@staticmethod
	def get_all_matches():
		db_client = DbClient.get_client()
		cursor = db_client.league.pro_matches.find()
		return cursor
	
	## return all matches not marked as is_test
	@staticmethod
	def get_training_set():
		db_client = DbClient.get_client()
		cursor = db_client.league.pro_matches.find({"is_test" : False})
		return cursor
	
	## return all matches that are labeled is_test
	@staticmethod
	def get_test_set():
		db_client = DbClient.get_client()	
		cursor = db_client.league.pro_matches.find({"is_test" : True})
		return cursor
	
	## add new match to db 
	def create_pro_match(self):
		db_client = DbClient.get_client()
		record = db_client.league.pro_matches.insert_one({
			"description" : self.description,
			"champs1" : self.champs1,
			"champs2" : self.champs2,
			"win" : self.win,
			"region" : self.region,
			"patch" : self.patch,
			"date_created" : self.date_created,
			"is_test" : self.is_test
			})
		print "Created pro match"
		return record.inserted_id
