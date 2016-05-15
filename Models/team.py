## Team: id, summoners, matches, date_created 
## list of summoners that plays together and the matches they have played
## defined uniquely by list of Summoners

from db_client import DbClient

class Team:
	def __init__(self, summoners, matches, date_created = None, id = None):
		self.id = id
		self.summoners = summoners
		self.matches = matches
		self.date_created = time.time()

	@classmethod
	def from_dict(cls, d):
		id = d["_id"]
		summoners = d["summoners"]
		matches = d["matches"]
		date_created = d["date_created"]
		return cls(summoners, matches, date_created, id)

	
	## if team already exists in db return it, otherwise return a new team
	@classmethod
	def get_team(cls, summoners):
		with DbClient() as db_client:
			cursor = db_client.find_team(summoners)
		
		##if doesn't exist in db
		if cursor.count() == 0:
			##match list will have to be populated somewhere else
			return cls(summoners, [])
		else:
			##create model from summoner data in db
			assert (cursor.count() >= 1), "Error constructing Summoner model from cursor. Cursor is empty."
			team = cls.from_dict(cursor[0])
			return team

	## add new matches from list to existing list of matches
	def update_matches(self, new_matches):
		updated_matches = self.matches + new_matches
		self.matches = updated_matches
	
	## push team into database
	def save(self):
		with DbClient() as db_client:
			#if already exists in db
			if self.id != None:
				db_client.update_team(self.id, self.matches)
			else:
				self.id = db_client.create_team(self.summoners, self.matches, self.date_created)
