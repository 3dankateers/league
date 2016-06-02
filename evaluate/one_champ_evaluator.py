############################################################################
## prints results of evaluating team comp based on winrates of each champ 
############################################################################
from champ import Champ
from evaluator import Evaluator
from champ_winrate_calculator import ChampWinrateCalculator

CONF_THRESHOLD = 0.02
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

	## return 100 if team1 is favoured, else return 200
	def predict_winner(self):
		return self.winner

	##return true if confident in predicted winner, otherwise false
	def is_confident(self):
		if abs(self.ti1.aggregate_winrate - self.ti2.aggregate_winrate) > CONF_THRESHOLD:
			return True
		else:
			return False

	@staticmethod
	def retrain():
		winrate_calc = ChampWinrateCalculator()
		winrate_calc.run()
		

	## calculate winrates needed
	## process each team independently
	def process(self):
		self.process_team(self.ti1)
		self.process_team(self.ti2)
		self.normalize_winrates()

		if self.ti1.aggregate_winrate > self.ti2.aggregate_winrate:
			self.winner = 100
		else:
			self.winner = 200

	def normalize_winrates(self):
		winrate1 = self.ti1.aggregate_winrate
		winrate2 = self.ti2.aggregate_winrate
		self.ti1.aggregate_winrate = winrate1/(winrate1 + winrate2)
		self.ti2.aggregate_winrate = winrate2/(winrate1 + winrate2)


	##calculates all neccesary team info and updates ti (teaminfo)
	def process_team(self, ti):
		for i,champ_id in enumerate(ti.champ_ids):
			cursor = Champ.find_champ(champ_id)
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

