############################################################################
## prints results of evaluating team comp based on winrates of each champ 
############################################################################
from db_client import DbClient
from champ import Champ
from evaluator import Evaluator

ONE_CHAMP_SAMPLE_LIMIT = 20

##stores information calculated in process()
class TeamInfo:
	def __init__(self, champ_ids):
		self.champ_ids = champ_ids
		self.winrates = [-1] * 5
		self.aggregate_winrate = 0
		self.total_winrate = 0
		self.num_champs_considered = 0
	
	def update_aggregate_winrate(self):
		for r in self.winrates:
			if r != -1:
				self.total_winrate += r
		self.aggregate_winrate = self.total_winrate/self.num_champs_considered
				
	def print_result(self):
		for i,id in enumerate(self.champ_ids):
			if (self.winrates[i] != -1):
				print id, " ", str(self.winrates[i])
			else:
				print id, " not enough winrate data"
			
		print "Normalized win rate = ", str(self.aggregate_winrate)


class OneChampEvaluator(Evaluator):
	
	def __init__(self, champs1_ids, champs2_ids):
		self.ti1 = TeamInfo(champs1_ids)
		self.ti2 = TeamInfo(champs2_ids)
		self.winner = 100

	## return 1 if team1 is favoured, else return 2
	def predict_winner(self):
		return self.winner
	
	## calculate winrates needed
	## process each team independently
	def process(self):
		self.process_team(self.ti1)
		self.process_team(self.ti2)
		if self.ti1.aggregate_winrate > self.ti2.aggregate_winrate:
			self.winner = 100
		else:
			self.winner = 200


	##calculates all neccesary team info and updates ti (teaminfo)
	def process_team(self, ti):
		with DbClient() as db_client:
			for i,champ_id in enumerate(ti.champ_ids):
				cursor = Champ.find_champ(db_client, champ_id)
				champ = Champ.from_dict(cursor[0])
				if (champ.winrate != None) and (champ.winrate_sample_size > ONE_CHAMP_SAMPLE_LIMIT):
					ti.winrates[i] = champ.winrate
					ti.num_champs_considered += 1
		ti.update_aggregate_winrate()

	def print_results(self):
		print "#################################################################################"
		print "One Champ Results: "
		print "Team1"
		self.ti1.print_result()
		print "#########################################################"
		print "Team2"
		self.ti2.print_result()
		print "#################################################################################"

