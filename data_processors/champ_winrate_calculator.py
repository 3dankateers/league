############################################################################
## analyzes data from matches db and calculates winrates for each champ
## inserts winrates into db
############################################################################
from champ import Champ
from match import Match
from pro_match import ProMatch

PROMATCH_MULTIPLIER = 0 
MATCH_MULTIPLIER = 1 

class ChampWinrateCalculator:
	
	def __init__(self, prediction_target, premade_only):
		##hash counts wins and losses for each champ
		self.losses = {}
		self.wins = {}
		self.prediction_target = prediction_target
		self.premade_only = premade_only
		
		##make pro_matches count for more than normal matches

	def run(self):
		##reset winrates and then recalculate
		Champ.reset_winrates()
		self.count_all_matches(Match)
		self.count_all_matches(ProMatch)
		self.update_winrates()
	
	##populate losses and wins with the information from each match in db
	def count_all_matches(self, match_class):
		cursor = match_class.get_training_set(self.premade_only)
		print "Training champ winrates with training cases: ", cursor.count()
		
		for d in cursor:
			match = match_class.from_dict(d)
			c1 = match.champs1
			c2 = match.champs2
			## 100 means team1 won, 200 means team2 won
			if self.prediction_target == Match.WIN: 
				win = match.win
			else:
				win = match.first_blood
			
			if win  == 100:
				self.add_champs_to_dict(self.wins, match_class, c1)
				self.add_champs_to_dict(self.losses, match_class, c2)
			elif win == 200:
				self.add_champs_to_dict(self.losses, match_class, c1)
				self.add_champs_to_dict(self.wins, match_class, c2)

	
	def add_champs_to_dict(self, d, match_class, champs):
		
		## weigh pro matches more than ordinary matches
		if match_class == Match:
			multiplier = MATCH_MULTIPLIER
		else:
			multiplier = PROMATCH_MULTIPLIER
		
		
		for c in champs:
			if c in d:
				##count another win/loss for that champ
				d[c]+= (1*multiplier)
			else:
				##first occurance of that champ
				d[c] = (1*multiplier)

	##update db champ with a new winrate and sample size fot that winrate
	def update_winrates(self):
			for key, value in self.wins.iteritems():
				##make sure key is present in both dicts
				if key in self.losses:
					cursor = Champ.find_champ(key)
					champ = Champ.from_dict(cursor[0])
					sample_size = value + self.losses[key]
					if sample_size > 0:
						winrate = value / float(sample_size)
					else:
						winrate = 0.5
					champ.winrate = winrate
					champ.winrate_sample_size = sample_size
					champ.save()
					##print "Updated ", champ.name, ". Winrate: ", str(champ.winrate), ". Size: ", str(champ.winrate_sample_size)

	

