############################################################################
## analyzes data from matches db and calculates winrates for each champ
## inserts winrates into db
############################################################################
from db_client import DbClient
from champ import Champ
from match import Match

class ChampWinrateCalculator:
	
	def __init__(self):
		##hash counts wins and losses for each champ
		self.losses = {}
		self.wins = {}

	def run(self):
		self.count_all_matches()
		self.update_winrates()
	
	##populate losses and wins with the information from each match in db
	def count_all_matches(self):
		with DbClient() as db_client:
			cursor = db_client.get_all_matches()
			for d in cursor:
				match = Match.from_dict(d)
				c1 = match.champs1
				c2 = match.champs2
				## 100 means team1 won, 200 means team2 won
				win = match.win
				if win  == 100:
					ChampWinrateCalculator.add_champs_to_dict(self.wins, c1)
					ChampWinrateCalculator.add_champs_to_dict(self.losses, c2)
				elif win == 200:
					ChampWinrateCalculator.add_champs_to_dict(self.losses, c1)
					ChampWinrateCalculator.add_champs_to_dict(self.wins, c2)

	
	@staticmethod
	def add_champs_to_dict(d, champs):
		for c in champs:
			if c in d:
				##count another win/loss for that champ
				d[c]+= 1
			else:
				##first occurance of that champ
				d[c] = 1

	##update db champ with a new winrate and sample size fot that winrate
	def update_winrates(self):
		for key, value in self.wins.iteritems():
			##make sure key is present in both dicts
			if key in self.losses:
				with DbClient() as db_client:
					cursor = db_client.find_champ(key)
					champ = Champ.from_dict(cursor[0])
				sample_size = value + self.losses[key]
				winrate = value / float(sample_size)
				champ.winrate = winrate
				champ.winrate_sample_size = sample_size
				champ.save()
				print "Updated ", champ.name, ". Winrate: ", str(champ.winrate), ". Size: ", str(champ.winrate_sample_size)

	

