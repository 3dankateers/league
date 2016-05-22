## match : id, team1, team2, champs1, champs2, duration, win, gametype, region, patch, tier, date, is_test

from db_client import DbClient

class Match:
	def __init__(self, id, team1, team2, champs1, champs2, duration, win, gametype, region, patch, tier, date, is_test = False):
		self.id = id
		self.team1 = team1
		self.team2 = team2
		self.champs1 = champs1
		self.champs2 = champs2
		self.duration = duration
		self.win = win
		self.gametype = gametype
		self.region = region
		self.patch = patch
		self.tier = tier
		self.date = date
		self.is_test = is_test
	
	@classmethod
	def from_dict(cls, d):
		id = d["_id"]
		team1 = d["team1"]
		team2 = d["team2"]
		champs1 = d["champs1"]
		champs2 = d["champs2"]
		duration = d["duration"]
		win = d["win"]
		gametype = d["gametype"]
		region = d["region"]
		patch = d["patch"]
		tier = d["tier"]
		date = d["date"]
		is_test = d["is_test"]
			
		return cls(id, team1, team2, champs1, champs2, duration, win, gametype, region, patch, tier, date, is_test)

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
		with DbClient() as db_client:
			record = db_client.db.matches.insert_one({
				"_id" : self.id,
				"team1" : self.team1,
				"team2" : self.team2,
				"champs1" : self.champs1,
				"champs2" : self.champs2,
				"duration" : self.duration,
				"win" : self.win,
				"gametype" : self.gametype,
				"region" : self.region,
				"patch" : self.patch,
				"tier" : self.tier,
				"date" : self.date,
				"is_test" : self.is_test
				})
			print "Created match"
	
	## update existing pair with new values 
	def update_match(self):
		with DbClient() as db_client:
			db_client.db.matches.update_one(
					{"_id" : self.id},{
						"$set": {
							"is_test" : self.is_test,
							}
					})
			print "Updated match." 

	
	## find match and return it based on id
	@staticmethod
	def find_match(id):
		with DbClient() as db_client:
			cursor = db_client.db.matches.find({"_id" : id})
			return cursor
	
	## return all matches
	@staticmethod
	def get_all_matches():
		with DbClient() as db_client:	
			cursor = db_client.db.matches.find()
			return cursor
	
	## return all matches that are labeled is_test
	@staticmethod
	def get_all_tests():
		with DbClient() as db_client:	
			cursor = db_client.db.matches.find({"is_test" : True})
			return cursor
