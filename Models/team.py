## Team: id, player_ids, match_ids, sides, date_created 
## list of player_ids that plays together and the match_ids they have played
## defined uniquely by list of Summoners

from db_client import DbClient
import time

class Team:
	def __init__(self, player_ids, match_ids, sides, date_created = None, id = None):
		self.id = id
		self.player_ids = player_ids
		self.match_ids = match_ids
		self.sides = sides
		self.date_created = time.time()

	@classmethod
	def from_dict(cls, d):
		id = d["_id"]
		player_ids = d["player_ids"]
		match_ids = d["match_ids"]
		sides = d["sides"]
		date_created = d["date_created"]
		return cls(player_ids, match_ids, sides, date_created, id)

	
	## if team already exists in db return it, otherwise return a new team
	@classmethod
	def get_team(cls, player_ids, match_ids, sides):
		db_client = DbClient.get_client()
		cursor = Team.find_team(player_ids)
		
		##if doesn't exist in db
		if cursor.count() == 0:
			return cls(player_ids, match_ids, sides)
		else:
			##create model from summoner data in db
			assert (cursor.count() >= 1), "Error constructing Summoner model from cursor. Cursor is empty."
			team = cls.from_dict(cursor[0])
			return team

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
				"player_ids" : self.player_ids,
				"match_ids" : self.match_ids,
				"sides" : self.sides,
				"date_created" : self.date_created
			})
		print("Created new team with ", str(len(self.match_ids)), " match_ids.")
		return record.inserted_id

	
	## update existing team with new values passed in
	def update_team(self):
		db_client = DbClient.get_client()
		db_client.league.teams.update_one(
				{"_id" : self.id},{
					"$set": {
						"match_ids" : self.match_ids,
						"sides" : self.sides
						}
				})
		print("Updated team")

	## find team and return it based on list of player_ids
	@staticmethod
	def find_team(player_ids):
		db_client = DbClient.get_client()
		cursor = db_client.league.teams.find({"player_ids" : player_ids})
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

