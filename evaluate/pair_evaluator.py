############################################################################
## evaluate 2 team comps based on pairs of champions 
############################################################################

from db_client import DbClient
from pair import Pair

PAIR_SAMPLE_LIMIT = 1

##helper class to store results for each team comp
class TeamWinrateInfo:
	def __init__(self, team_comp):
		self.team_comp = team_comp
		self.num_relevant_pairs = 0
		self.total_winrate = 0
		self.aggregate_winrate = 0
	
	def update_aggregate_winrate(self):
		self.aggregate_winrate = self.total_winrate/self.num_relevant_pairs


class PairEvaluator:

	def __init__(self, team1, team2):
		self.team1_ally_info = TeamWinrateInfo(team1)
		self.team2_ally_info = TeamWinrateInfo(team2)
		
		self.team1_enemy_info = TeamWinrateInfo(team1)
		self.team2_enemy_info = TeamWinrateInfo(team2)
	
	##processes each team comp in turn
	def process_teams(self):
		print "Processing pairs in team comp ..."
		self.process_winrate_allies(self.team1_ally_info)
		self.process_winrate_allies(self.team2_ally_info)
		self.process_winrate_enemies(self.team1_enemy_info, self.team2_enemy_info)

	## prints winrate calculation results
	def print_results(self):
		self.process_teams()
		print "#################################################################################"
		print "Pair Analysis Results: "
		print "Team1"
		print "Ally Winrate Aggregate: ", str(self.team1_ally_info.aggregate_winrate)
		print "Enemy Winrate Aggregate: ", str(self.team1_enemy_info.aggregate_winrate)
		print "#########################################################"
		print "Team2"
		print "Ally Winrate Aggregate: ", str(self.team2_ally_info.aggregate_winrate)
		print "Enemy Winrate Aggregate: ", str(self.team2_enemy_info.aggregate_winrate)
		print "#################################################################################"

	## takes team_ally_info and processes it by calculating all ally winrates
	def process_winrate_allies(self, twi):
		with DbClient() as db_client:
			champs = twi.team_comp
			for c1 in champs:
				for c2 in champs:
					if c1 != c2:
						## create all possible combinations of pairs from team comp
						pair_id = Pair.calc_id(c1,c2,"ally")
						cursor = Pair.find_pair(db_client, pair_id)
						if cursor.count() > 0:
							pair = Pair.from_dict(cursor[0])

							##make sure pair same size is statistically significant
							if pair.winrate_sample_size > PAIR_SAMPLE_LIMIT:
								twi.total_winrate += pair.winrate
								twi.num_relevant_pairs += 1
			
			if twi.num_relevant_pairs > 0:
				twi.update_aggregate_winrate()	
	
	## takes 2 team_winrate_info and processes enemy winrates
	def process_winrate_enemies(self, twi1, twi2):
		with DbClient() as db_client:
			champs1 = twi1.team_comp
			champs2 = twi2.team_comp
			for c1 in champs1:
				for c2 in champs2:
						## create all possible combinations of pairs from 2 team comps
						pair_id = Pair.calc_id(c1,c2,"ally")
						cursor = Pair.find_pair(db_client, pair_id)

						##only look at winrates if we can find pair in db 
						if cursor.count() > 0:
							pair = Pair.from_dict(cursor[0])

							##make sure pair same size is statistically significant
							if pair.winrate_sample_size > PAIR_SAMPLE_LIMIT:
								## winrate doesn't need to be inversed since c1 remains c1 in pair_tuple
								if pair.pair_tuple[0] == c1:
									twi1.total_winrate += pair.winrate
									twi1.num_relevant_pairs += 1
									twi2.total_winrate += (1- pair.winrate)
									twi2.num_relevant_pairs += 1
								elif pair.pair_tuple[0] == c2:
									twi1.total_winrate += (1 - pair.winrate)
									twi1.num_relevant_pairs += 1
									twi2.total_winrate += pair.winrate
									twi2.num_relevant_pairs += 1
			
			if twi1.num_relevant_pairs > 0:
				twi1.update_aggregate_winrate()
			if twi2.num_relevant_pairs > 0:
				twi2.update_aggregate_winrate()



