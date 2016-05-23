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
			coordinates = []
			winner = match.win


			with DbClient() as db_client:
				cursor = Champ.get_all_champs()
				for c in cursor:
					champ = Champ.from_dict(c)
					if champ.id in match.champs1:
						coordinates.append(-1)
					elif champ.id in match.champs2:
						coordinates.append(1)
					else:
						coordinates.append(0)
			mhp = MatchHyperpoint(match_id, coordinates, winner)
			mhp.save()


