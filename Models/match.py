## match : id, team1, team2, champs1, champs2, first_blood, duration, win, gametype, region, patch, tier, date, is_team1, is_team2, is_test

from db_client import DbClient

class Match:

	##prediction target possibilities
	WIN = "win"
	FIRST_BLOOD = "first_blood"
	
	def __init__(self, id, team1, team2, champs1, champs2, first_blood, duration, win, gametype, region, patch, tier, date, is_team1 = False, is_team2 = False, is_test = False):
		self.id = id
		self.team1 = team1
		self.team2 = team2
		self.champs1 = champs1
		self.champs2 = champs2
		self.first_blood = first_blood
		self.duration = duration
		self.win = win
		self.gametype = gametype
		self.region = region
		self.patch = patch
		self.tier = tier
		self.date = date
		self.is_team1 = is_team1
		self.is_team2 = is_team2
		self.is_test = is_test
	
	@classmethod
	def from_dict(cls, d):
		id = d["_id"]
		team1 = d["team1"]
		team2 = d["team2"]
		champs1 = d["champs1"]
		champs2 = d["champs2"]
		first_blood = d["first_blood"]
		duration = d["duration"]
		win = d["win"]
		gametype = d["gametype"]
		region = d["region"]
		patch = d["patch"]
		tier = d["tier"]
		date = d["date"]
		is_team1 = d["is_team1"]
		is_team2 = d["is_team2"]
		is_test = d["is_test"]
			
		return cls(id, team1, team2, champs1, champs2, first_blood, duration, win, gametype, region, patch, tier, date, is_team1, is_team2, is_test)

	## if match already exists in db return it, otherwise return None(caller will have to create game himself)
	@classmethod
	def get_match(cls, id):
		cursor = Match.find_match(id)
		
		##if doesn't exist in db
		if cursor.count() == 0:
			return None
		else:
			##create model from summoner data in db
			assert (cursor.count() >= 1), "Error constructing Summoner model from cursor. Cursor is empty."
			match = cls.from_dict(cursor[0])
			
			return match

	## push match into database
	def save(self):
		cursor = Match.find_match(self.id)
		if cursor.count() == 0:
			self.create_match()
		else:
			self.update_match()
	
	
	## add new match to db 
	def create_match(self):
		db_client = DbClient.get_client()
		record = db_client.league.matches.insert_one({
			"_id" : self.id,
			"team1" : self.team1,
			"team2" : self.team2,
			"champs1" : self.champs1,
			"champs2" : self.champs2,
			"first_blood" : self.first_blood,
			"duration" : self.duration,
			"win" : self.win,
			"gametype" : self.gametype,
			"region" : self.region,
			"patch" : self.patch,
			"tier" : self.tier,
			"date" : self.date,
			"is_team1" : self.is_team1,
			"is_team2" : self.is_team2,
			"is_test" : self.is_test
			})
		print "Created match"
	
	## update existing pair with new values 
	def update_match(self):
		db_client = DbClient.get_client()	
		db_client.league.matches.update_one(
				{"_id" : self.id},{
					"$set": {
						"is_test" : self.is_test,
						"is_team1" : self.is_team1,
						"is_team2" : self.is_team2
						}
				})
		##print "Updated match." 

	
	## find match and return it based on id
	@staticmethod
	def find_match(id):
		db_client = DbClient.get_client()
		cursor = db_client.league.matches.find({"_id" : id})
		return cursor
	
	## return all matches
	@staticmethod
	def get_all_matches():
		db_client = DbClient.get_client()
		cursor = db_client.league.matches.find()
		return cursor
	
	## return all matches to be used for training models
	@staticmethod
	def get_training_set():
		db_client = DbClient.get_client()
		cursor = db_client.league.matches.find({"is_test" : False})
		return cursor

	##return set that should be considered when deciding what is part of test set and what is training set
	@staticmethod
	def get_testable_set():
		return Match.get_all_matches()
	
	##reset is_test of all matches to w/e is passed in
	@staticmethod
	def reset_all_tests(is_test = True):
		db_client = DbClient.get_client()
		db_client.league.matches.update_many(
				{},{
					"$set": {
						"is_test" : is_test
						}
				})

	## return all matches that are labeled is_test
	@staticmethod
	def get_test_set():
		db_client = DbClient.get_client()	
		cursor = db_client.league.matches.find({"is_test" : True})
		return cursor
