############################################################################
## turn all training matches into hyperpoints  
## inserts hyperpoints into db
############################################################################
from match import Match
from champ import Champ
from match_hyperpoint import MatchHyperpoint

class HyperpointCalculator:
	def __init__(self, match_class, prediction_target = Match.WIN):
		self.prediction_target = prediction_target
		self.match_class = match_class

	def run(self):
		##delete old hyperpoints
		MatchHyperpoint.delete_all()
		cursor = self.match_class.get_training_set()
		print("Training hyperpoints with training cases: ", cursor.count())

		for m in cursor:
			match = self.match_class.from_dict(m)
			
			match_id = match.id
			coordinates = MatchHyperpoint.get_coordinates(match.champs1, match.champs2)
			if self.prediction_target == Match.WIN: 
				winner = match.win
			elif self.prediction_target == Match.FIRST_BLOOD:
				winner = match.first_blood
			
			mhp = MatchHyperpoint(match_id, coordinates, winner)
			mhp.save()
	
 
