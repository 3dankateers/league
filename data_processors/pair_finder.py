############################################################################ 
## populates db with pairs
## calculates win rates from match data
## updates db pair entries with winrates
############################################################################
from db_client import DbClient
from champ import Champ
from pair import Pair

class PairFinder:

	def __init__(self):
		##dicts used to count pair of enemies
		self.enemy_wins = {}
		self.enemy_losses = {}
		##dicts used to count pair of enemies
		self.ally_wins = {}
		self.ally_losses = {}
	
	def run(self):
		self.populate_db_with_pairs()

	def populate_db_with_pairs():
		with DbClient as db_client:
			cursor1 = db_client.find_all_champs()
			for di in cursor1:
				cursor2 = db_client.find_all_champs()
				for dj in cursor2:
					##compare n^2 champs to find all possible pairs and make champ is not paired with itself
					if di != dj:
						champ1 = Champ.from_dict(di)
						champ2 = Champ.from_dict(dj)
						##check that it is not already
						if (db_client.find_pair(champ1, champ2, "ally").count() == 0) and
						


