############################################################################
## passed in a certain type of evaluator, simulate bets on pro matches 
## print results
############################################################################

from pro_match import ProMatch
from underdog_evaluator import UnderdogEvaluator
from aggregate_evaluator import AggregateEvaluator

BET_AMOUNT = 100

class BetSimulator:
	def __init__(self, evaluator_class, need_confidence = False):
		self.evaluator_class = evaluator_class
		self.money_total = 0
		self.total_confident_bets = 0
		self.total_bets = 0
		self.bets_won = 0
		self.bets_lost = 0
		self.need_confidence = need_confidence
	
	def run(self):
		self.make_bets()
	
	def make_bets(self):
		cursor = ProMatch.get_bettable_set()
		self.total_bets = cursor.count()

		for m in cursor:
			match = ProMatch.from_dict(m)
			
			##underdog evaluator takes in different input so need special case
			if self.evaluator_class == UnderdogEvaluator:	
				evaluator = self.evaluator_class(match)
			elif self.evaluator_class == AggregateEvaluator:
				evaluator = self.evaluator_class(match.champs1, match.champs2, match)
			else:
				evaluator = self.evaluator_class(match.champs1, match.champs2)
			
			team1_ml = float(match.get_latest_ML_T1())
			team2_ml = float(match.get_latest_ML_T2())
			evaluator.process()
			##only count test matches if either confidence is not needed( if it is make sure evaluator is confident)
			if((not self.need_confidence) or evaluator.is_confident()):
				self.total_confident_bets += 1
				winner_predicted = evaluator.predict_winner()
				actual_winner = match.win
				
				
				if(winner_predicted == actual_winner):
					self.bets_won += 1
					if actual_winner == 100:
						if team1_ml > 0:
							self.money_total += team1_ml
						else:
							self.money_total += BET_AMOUNT*100/float(abs(team1_ml))
					elif actual_winner == 200:
						if team2_ml > 0:
							self.money_total += team2_ml
						else:
							self.money_total += BET_AMOUNT*100/float(abs(team2_ml))
				else:
					self.bets_lost += 1
					self.money_total -= 100



	def print_results(self):
		print "Total Bets Considered", self.total_bets
		print "Total Bets Made", self.total_confident_bets
		print "Money Risked", self.total_bets * 100
		print "Win Percentage", 100*self.bets_won/float(self.bets_lost + self.bets_won)
		print "Profit", self.money_total 
		print ""
		print ""




