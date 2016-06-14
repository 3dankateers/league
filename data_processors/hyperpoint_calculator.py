############################################################################
## turn all training matches into hyperpoints  
## inserts hyperpoints into db
############################################################################
from match import Match
from champ import Champ
from match_hyperpoint import MatchHyperpoint

class HyperpointCalculator:
	def __init__(self, prediction_target):
		self.prediction_target = prediction_target
		pass

	def run(self):
		##delete old hyperpoints
		MatchHyperpoint.delete_all()
		cursor = Match.get_training_set()

		for m in cursor:
			match = Match.from_dict(m)
			
			match_id = match.id
			coordinates = MatchHyperpoint.get_coordinates(match.champs1, match.champs2)
			if self.prediction_target == Match.WIN: 
				winner = match.win
			elif self.prediction_target == Match.FIRST_BLOOD:
				winner = match.first_blood
			
			mhp = MatchHyperpoint(match_id, coordinates, winner)
			mhp.save()
	
 
