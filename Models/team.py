## Team: id, summoners, matches, date_created 
## list of summoners that plays together and the matches they have played
## defined uniquely by list of Summoners

from db_client import DbClient
import time

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
		db_client = DbClient.get_client()
		cursor = Team.find_team(summoners)
		
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
		updated_matches = list(set(self.matches) | set(new_matches))
		self.matches = updated_matches
	
	## push team into database
	def save(self):
		#if already exists in db
		if self.id != None:
			self.update_team()
		else:
			self.id = self.create_team()
	
	
	def create_team(self):
		db_client = DbClient.get_client()	
		record = db_client.league.teams.insert_one({
				"summoners" : self.summoners,
				"matches" : self.matches,
				"date_created" : self.date_created
			})
		print "Created new team with ", str(len(self.matches)), " matches."
		return record.inserted_id

	
	## update existing team with new values passed in
	def update_team(self):
		db_client = DbClient.get_client()
		db_client.league.teams.update_one(
				{"_id" : self.id},{
					"$set": {
						"matches" : self.matches
						}
				})
		print "Updated team" 

	## find team and return it based on list of summoners
	@staticmethod
	def find_team(summoners):
		db_client = DbClient.get_client()
		cursor = db_client.league.teams.find({"summoners" : summoners})
		return cursor

	@staticmethod
	def get_all_teams():
		db_client = DbClient.get_client()
		cursor = db_client.league.teams.find()
		return cursor

	##clears team collection
	## usually ran before teams are recalculated
	@staticmethod
	def drop_all():
		db_client = DbClient.get_client()
		db_client.league.teams.drop()

