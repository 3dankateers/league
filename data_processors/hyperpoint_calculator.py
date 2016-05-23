############################################################################
## turn all training matches into hyperpoints  
## inserts hyperpoints into db
############################################################################
from db_client import DbClient
from match import Match
from champ import Champ
from match_hyperpoint import MatchHyperpoint

class HyperpointCalculator:
	def __init__(self):
		pass

	def run(self):
		with DbClient() as db_client:
			cursor = Match.get_training_set()
		for m in cursor:
			match = Match.from_dict(m)
			
			match_id = match.id
			coordinates = MatchHyperpoint.get_coordinates(match.champs1, match.champs2)
			winner = match.win
			

			mhp = MatchHyperpoint(match_id, coordinates, winner)
			mhp.save()
	
 
