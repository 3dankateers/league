## match_hyperpoint: id, match_id, coordinates, winner
## point in n dimensional space representing the champions picked by a team
## at position i, coordinates[i] = -1 means team 1 has champ, 0 means no team has champ, 1 means team2 has champ


from db_client import DbClient
from champ import Champ

class MatchHyperpoint:

	def __init__(self, match_id, coordinates, winner, id = None):
		self.match_id = match_id
		self.coordinates = coordinates
		self.winner = winner
		self.id = id	

	@classmethod
	def from_dict(cls, d):
		id = d["_id"]
		match_id = d["match_id"]
		coordinates = d["coordinates"]
		winner = d["winner"]
		return cls(match_id, coordinates, winner, id)

	## push match_hyperpoint into database
	def save(self):
		self.id = self.create_match_hyperpoint()
	
	
	## add new match to db 
	def create_match_hyperpoint(self):
		with DbClient() as db_client:
			record = db_client.db.matches_hyperpoints.insert_one({
				"match_id" : self.match_id,
				"coordinates" : self.coordinates,
				"winner" : self.winner
				})
			print "Created match_hyperpoint"
		return record.inserted_id
	
	
	## return all match_hyperpoints
	@staticmethod
	def get_all():
		with DbClient() as db_client:	
			cursor = db_client.db.matches_hyperpoints.find()
			return cursor

	
