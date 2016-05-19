############################################################################
## prints results of evaluating team comp based on winrates of each champ 
############################################################################
from db_client import DbClient
from champ import Champ

ONE_CHAMP_SAMPLE_LIMIT = 20

class OneChampEvaluator:
	
	## print one champ simple analysis results for a team comp
	@staticmethod
	def print_one_champ_result(t):
		total_winrate = 0
		num_champs_considered = 0

		for champ_name in t:
			with DbClient() as db_client:
				cursor = Champ.find_champ_by_name(champ_name)
			try:
				champ = Champ.from_dict(cursor[0])
			except:
				print "Mistyped champ name: ", champ_name

			if (champ.winrate != None) and (champ.winrate_sample_size > ONE_CHAMP_SAMPLE_LIMIT):
				total_winrate += champ.winrate
				num_champs_considered += 1
				print champ.name, " ", str(champ.winrate)
			else:
				print champ.name, " not enough winrate data"
			
		print "Normalized win rate = ", str(total_winrate / num_champs_considered)
