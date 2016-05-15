############################################################################
## given team comp
## display various metrics to evaluate the team comp
############################################################################

from champ import Champ
from db_client import DbClient

ONE_CHAMP_SAMPLE_LIMIT = 20


class CompEvaluator:
	
	def __init__(self, team1, team1):
		self.team1 = team1
		self.team2 = team2
	
	def run(self):
		##Print simple 1 champ winrate aggregate
		
		print "One Champ Results: "
		print "Team1"
		print_one_champ_results(team1)
		print "Team2"
		print_one_champ_results(team2)

	
	## print one champ simple analysis results for a team comp
	def print_one_champ_result(t):
		total_winrate = 0
		num_champs_considered = 0

		for champ_name in t:
			cursor = db_client.find_champ_by_name(champ_name)
			try:
				champ = Champ.from_dict(cursor[0])
			except:
				print "Mistyped champ name: ", champ_name

			if (champ.winrate != None) and (champ.winrate_sample_size > ONE_CHAMP_SAMPLE_LIMIT):
				total_winrate += champ.winrate
				num_champs_considered += 1
				print champ.name, " ", str(winrate)
			else:
				print champ.name, " not enough winrate data"
			
			print "Normalized win rate = ", str(total_winrate / num_champs_considered)
				

