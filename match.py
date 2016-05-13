## match : id, league_id, team1, team2, champs1, champs2, duration, win, gametype, tier, date

class Match:
	def __init__(self, league_id, team1, team2, champs1, champs2, duration, win, gametype, tier, date, id = None):
		self.id = id
		self.league_id = league_id
		self.team1 = team1
		self.team2 = team2
		self.champs1 = champs1
		self.champs2 = champs2
		self.duration = duration
		self.win = win
		self.gametype = gametype
		self.tier = tier
		self.date = date
	
	@classmethod
	def from_object(cls, o):
		id = o["_id"]
		league_id = o["league_id"]
		team1 = o["team1"]
		team2 = o["team2"]
		champs1 = o["champs1"]
		champs2 = o["champs2"]
		duration = o["duration"]
		win = o["win"]
		gametype = o["gametype"]
		tier = o["tier"]
		date = o["date"]
			
		return cls(league_id, team1, team2, champs1, champs2, duration, win, gametype, tier, date, id)

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
			match = cls.from_object(cursor[0])
			
			return match
