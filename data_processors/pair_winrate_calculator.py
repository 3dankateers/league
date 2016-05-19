############################################################################ 
## populates db with pairs
## calculates win rates from match data
## updates db pair entries with winrates
############################################################################
from db_client import DbClient
from champ import Champ
from pair import Pair
from match import Match

class PairWinrateCalculator:

	def __init__(self):
		##dicts used to count pair of enemies
		self.enemy_wins = {}
		self.enemy_losses = {}
		##dicts used to count pair of enemies
		self.ally_wins = {}
		self.ally_losses = {}
	
	def run(self):
		self.count_matches()
		self.update_winrates(self.ally_wins, self.ally_losses, "ally")
		self.update_winrates(self.enemy_wins, self.enemy_losses, "enemy")
	
	
	##update db pairs with a new winrate and sample size fot that winrate
	## type = "ally" or "enemy", and d_wins and d_losses are the correponding dictionaries for ally or enemy
	def update_winrates(self, d_wins, d_losses, type):
		for key, value in self.d_wins.iteritems():
			if key in d_losses:
				with DbClient() as db_client:
					pair = Pair.get_pair(key[0], key[1], type)
				sample_size = value + self.d_losses[key]
				winrate = value / float(sample_size)
				pair.winrate = winrate
				pair.winrate_sample_size = sample_size
				pair.save()
				print "Updated ", pair.pair_tuple, ". Winrate: ", str(pair.winrate), ". Size: ", str(pair.winrate_sample_size)

	def count_matches(self):
		with DbClient() as db_client:
			cursor = db_client.get_all_matches()
			for d in cursor:
				match = Match.from_dict(d)
				c1 = match.champs1
				c2 = match.champs2
				## 100 means team1 won, 200 means team2 won
				win = match.win
				
				## count ally pairs in match
				if win  == 100:
					self.add_ally_pairs_to_dict(self.ally_wins, c1)
					self.add_ally_pairs_to_dict(self.ally_losses, c2)
				elif win == 200:
					self.add_ally_pairs_to_dict(self.ally_wins, c2)
					self.add_ally_pairs_to_dict(self.ally_losses, c1)

				## count enemy pairs in match
				self.add_enemy_pairs_to_dict(win, c1, c2)
	
	## generate all pairs from champs 
	## increment the entries in the dictionary(d) that correspond to the pairs found in champs
	def add_ally_pairs_to_dict(self, d, champs):
		for c1 in champs:
			for c2 in champs:
				if c1 != c2:
					pair = Pair.get_pair(c1, c2, "ally")
					pair.save()
					pair_tuple = pair.pair_tuple
					
					##if pair was seen before
					if pair_tuple in d:
						d[pair_tuple] += 1
					else:
						d[pair_tuple] = 1


	## generate all enemy pairs from champs1, champs2 
	## increment the entries in the proper dictionaries that correspond to the pairs found in champs
	## win = 100 means champs1 team won, win = 200 means champs2 team won
	def add_enemy_pairs_to_dict(self, win, champs1, champs2):
		for c1 in champs1:
			for c2 in champs2:
				if c1 != c2:
					pair = Pair.get_pair(c1, c2, "enemy")
					pair.save()
					pair_tuple = pair.pair_tuple

					if win == 100:
						if pair_tuple[0] in champs1:
							##first champ in tuple is a winner
							PairWinrateCalculator.increment_dict(self.enemy_wins, pair_tuple)
						elif win  == 200:
							##first champ in tuple is a loser
							PairWinrateCalculator.increment_dict(self.enemy_losses, pair_tuple)
	
	##increment count in d for that specific pair
	@classmethod
	def increment_dict(d, pair_tuple):
		if pair_tuple in d:
			self.d[pair_tuple] += 1
		else:
			self.d[pair_tuple] = 1
					
