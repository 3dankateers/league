############################################################################ 
## populates db with pairs
## calculates win rates from match data
## updates db pair entries with winrates
############################################################################
from db_client import DbClient
from champ import Champ
from pair import Pair
from match import Match
from pro_match import ProMatch

PROMATCH_MULTIPLIER = 0 
MATCH_MULTIPLIER = 1 

class PairWinrateCalculator:

	def __init__(self, prediction_target):
		##dicts used to count pair of enemies
		self.enemy_wins = {}
		self.enemy_losses = {}
		##dicts used to count pair of enemies
		self.ally_wins = {}
		self.ally_losses = {}
		self.prediction_target = prediction_target
	
	def run(self):
		## drop everything at the start since everythinf is recalculated and inserted
		Pair.drop_all()
		self.count_matches(Match)
		self.count_matches(ProMatch)
		self.update_winrates(self.ally_wins, self.ally_losses, "ally")
		self.update_winrates(self.enemy_wins, self.enemy_losses, "enemy")
	
	
	##update db pairs with a new winrate and sample size fot that winrate
	## type = "ally" or "enemy", and d_wins and d_losses are the correponding dictionaries for ally or enemy
	def update_winrates(self, d_wins, d_losses, type):
		all_pairs_dicts = []
		unique_pairs_list = []
		for key, value in d_wins.iteritems():
			if key in d_losses:
				
				pair = Pair(key[0], key[1], type)
				tup = (pair.champ1, pair.champ2, pair.type)
				##make sure there are no duplicates
				if tup not in unique_pairs_list:
					unique_pairs_list.append(tup)
					sample_size = value + d_losses[key]
					winrate = value / float(sample_size)
					pair.winrate = winrate
					pair.winrate_sample_size = sample_size
					d = pair.to_dict()
					all_pairs_dicts.append(d)
					##print "Updated ", pair.pair_tuple, ". Winrate: ", str(pair.winrate), ". Size: ", str(pair.winrate_sample_size)
		
		##insert all pairs into db
		Pair.insert_all(all_pairs_dicts)

	def count_matches(self, match_class):
		cursor = match_class.get_training_set()
		for d in cursor:
			match = match_class.from_dict(d)
			c1 = match.champs1
			c2 = match.champs2
			## 100 means team1 won, 200 means team2 won
			if self.prediction_target == Match.WIN: 
				win = match.win
			else:
				win = match.first_blood
			
			## count ally pairs in match
			if win  == 100:
				self.add_ally_pairs_to_dict(self.ally_wins, c1, match_class)
				self.add_ally_pairs_to_dict(self.ally_losses, c2, match_class)
			elif win == 200:
				self.add_ally_pairs_to_dict(self.ally_wins, c2, match_class)
				self.add_ally_pairs_to_dict(self.ally_losses, c1, match_class)
			

			## count enemy pairs in match
			self.add_enemy_pairs_to_dict(win, c1, c2, match_class)

	
	## generate all pairs from champs 
	## increment the entries in the dictionary(d) that correspond to the pairs found in champs
	def add_ally_pairs_to_dict(self, d, champs, match_class):
		
		##weigh pro matches more than solo q matches
		if match_class == Match:
			multiplier = MATCH_MULTIPLIER 
		else:
			multiplier = PROMATCH_MULTIPLIER
		
		for c1 in champs:
			for c2 in champs:
				if c1 != c2:
					pair_tuple = Pair.calc_pair_tuple(c1,c2)	
					##if pair was seen before
					if pair_tuple in d:
						d[pair_tuple] += (1*multiplier)
					else:
						d[pair_tuple] = 1


	## generate all enemy pairs from champs1, champs2 
	## increment the entries in the proper dictionaries that correspond to the pairs found in champs
	## win = 100 means champs1 team won, win = 200 means champs2 team won
	def add_enemy_pairs_to_dict(self, win, champs1, champs2, match_class):
		for c1 in champs1:
			for c2 in champs2:
				if c1 != c2:
					pair_tuple = Pair.calc_pair_tuple(c1,c2)	

					if win == 100:
						if pair_tuple[0] in champs1:
							##first champ in tuple is a winner
							self.increment_dict(self.enemy_wins, pair_tuple, match_class)
						else:
							self.increment_dict(self.enemy_losses, pair_tuple, match_class)

					elif win  == 200:
						if pair_tuple[0] in champs1:
							##first champ in tuple is a loser
							self.increment_dict(self.enemy_losses, pair_tuple, match_class)
						else:
							self.increment_dict(self.enemy_wins, pair_tuple, match_class)
	
	##increment count in d for that specific pair
	def increment_dict(self, d, pair_tuple, match_class):
		##weigh pro matches more than solo q matches
		if match_class == Match:
			multiplier = 1
		else:
			multiplier = PROMATCH_MULTIPLIER
		
		if pair_tuple in d:
			d[pair_tuple] += (1*multiplier)
		else:
			d[pair_tuple] = 1
					
