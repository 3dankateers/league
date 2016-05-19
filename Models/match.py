## match : id, team1, team2, champs1, champs2, duration, win, gametype, region, patch, tier, date

from db_client import DbClient

class Match:
	def __init__(self, id, team1, team2, champs1, champs2, duration, win, gametype, region, patch, tier, date):
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
			
		return cls(id, team1, team2, champs1, champs2, duration, win, gametype, region, patch, tier, date)

	## if match already exists in db return it, otherwise return None(caller will have to create game himself)
	@classmethod
	def get_match(cls, id):
		with DbClient() as db_client:
			cursor = db_client.find_match(id)
		
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
		create_match()
	
	
	## add new match to db 
	def create_match():
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
				"date" : self.date
				})
			print "Created match"
	
	
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
