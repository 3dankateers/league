############################################################################
## evaluate 2 team comps based on pairs of champions 
############################################################################

from pair import Pair
from evaluator import Evaluator
from pair_winrate_calculator import PairWinrateCalculator

PAIR_SAMPLE_LIMIT = 20
CONF_THRESHOLD = 0.05

##helper class to store results for each team comp
class TeamWinrateInfo:
	def __init__(self, team_comp):
		self.team_comp = team_comp
		self.num_relevant_pairs = 0
		self.total_winrate = 0
		self.aggregate_winrate = 0
	
	def update_aggregate_winrate(self):
		self.aggregate_winrate = self.total_winrate/self.num_relevant_pairs


class AllyPairEvaluator(Evaluator):

	def __init__(self, team1, team2):
		self.team1_ally_info = TeamWinrateInfo(team1)
		self.team2_ally_info = TeamWinrateInfo(team2)

	@staticmethod
	def retrain(prediction_target, premade_only):
		winrate_calc = PairWinrateCalculator(prediction_target, premade_only)
		winrate_calc.run()
		

	##processes each team comp in turn
	def process(self):
		##print "Processing pairs in team comp ..."
		self.process_winrate_allies(self.team1_ally_info)
		self.process_winrate_allies(self.team2_ally_info)
		self.normalize_winrates()
		if self.team1_ally_info.aggregate_winrate > self.team2_ally_info.aggregate_winrate:
			self.winner = 100
		else:
			self.winner = 200

	## return 1 if team1 is favoured, else return 2
	def predict_winner(self):
		return self.winner
	
	def is_confident(self):
		if abs(self.team1_ally_info.aggregate_winrate - self.team2_ally_info.aggregate_winrate) > CONF_THRESHOLD:
			return True
		else:
			return False
	
	def normalize_winrates(self):
		winrate1 = self.team1_ally_info.aggregate_winrate
		winrate2 = self.team2_ally_info.aggregate_winrate
		if (winrate1  + winrate2) > 0:
			self.team1_ally_info.aggregate_winrate = winrate1/(winrate1 + winrate2)
			self.team2_ally_info.aggregate_winrate = winrate2/(winrate1 + winrate2)

	## prints winrate calculation results
	def print_results(self):
		self.process()
		print "#################################################################################"
		print " Ally Pair Evaluator Results: "
		print "Team1: " , str(self.team1_ally_info.aggregate_winrate)
		print "#########################################################"
		print "Team2:", str(self.team2_ally_info.aggregate_winrate)
		print "Difference: ", self.team1_ally_info.aggregate_winrate - self.team2_ally_info.aggregate_winrate
		print "WINNER: ", self.winner
		print "#################################################################################"

	## takes team_ally_info and processes it by calculating all ally winrates
	def process_winrate_allies(self, twi):
		champs = twi.team_comp
		for c1 in champs:
			for c2 in champs:
				if c1 != c2:
					## create all possible combinations of pairs from team comp
					pair_id = Pair.calc_id(c1,c2,"ally")
					cursor = Pair.find_pair(pair_id)
					if cursor.count() > 0:
						pair = Pair.from_dict(cursor[0])

						##make sure pair same size is statistically significant
						if pair.winrate_sample_size > PAIR_SAMPLE_LIMIT:
							twi.total_winrate += pair.winrate
							twi.num_relevant_pairs += 1
		
		if twi.num_relevant_pairs > 0:
			twi.update_aggregate_winrate()	

