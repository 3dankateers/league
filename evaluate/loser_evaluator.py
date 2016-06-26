##Note only works with ProMatches that have betting data, should only be called by simulate bets class
##Evaluator only bets on match 2 or 3 of a set of matches
## Always bets on team that just lost a game
## Always call this with confidence required

from evaluator import Evaluator
from pro_match import ProMatch

class LoserEvaluator(Evaluator):

	def __init__(self, match):
		self.match = match
		self.prev_match = self.find_prev_match()

	def find_prev_match(self):
		##if first match of set return none
		if self.match.map_number == 1:
			return None
		else:
			##get previous match in set
			prev_match = ProMatch.find_match(self.match.team1_name, self.match.team2_name, self.match.map_number - 1, self.match.match_day, "nitrogen")
			return prev_match


	## return 100 if team1 is favoured, else return 200
	def predict_winner(self):
		return self.winner
	
	##no training is neccesary for this evaluator
	@staticmethod
	def retrain(prediction_target, premade_only):
		pass

	##return true if confident in predicted winner, otherwise false
	def is_confident(self):
		if self.prev_match != None:
			return True
		else:
			return False

	## figure out who is the underdog and return
	def process(self):
		if self.prev_match != None:
			##predict winner = opposite of last game
			if self.prev_match.win == 100:
				self.winner = 200
			else:
				self.winner = 100
		else:
			self.winner = 200

	## nothing to print
	def print_results(self):
		pass
