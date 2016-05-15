## match : id, league_id, team1, team2, champs1, champs2, duration, win, gametype, region, patch, tier, date

from db_client import DbClient

class Match:
	def __init__(self, league_id, team1, team2, champs1, champs2, duration, win, gametype, region, patch, tier, date, id = None):
		self.id = id
		self.league_id = league_id
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
		league_id = d["league_id"]
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
			
		return cls(league_id, team1, team2, champs1, champs2, duration, win, gametype, region, patch, tier, date, id)

	## if match already exists in db return it, otherwise return None(caller will have to create game himself)
	@classmethod
	def get_match(cls, league_id):
		with DbClient() as db_client:
			cursor = db_client.find_match(league_id)
		
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
		with DbClient() as db_client:
			self.id = db_client.create_match(self.league_id, self.team1, self.team2, self.champs1, self.champs2, self.duration, self.win, self.gametype, self.region, self.patch, self.tier, self.date)
