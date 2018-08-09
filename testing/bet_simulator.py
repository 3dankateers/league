############################################################################
## passed in a certain type of evaluator, simulate bets on pro matches 
## print results
############################################################################

from pro_match import ProMatch
from underdog_evaluator import UnderdogEvaluator
from aggregate_evaluator import AggregateEvaluator
from loser_evaluator import LoserEvaluator

## if this is set to true, winnings are held constant at 100
##if false bet amout is held constant at 100
NORMALIZE_WINNINGS = False

class BetSimulator:
	def __init__(self, evaluator_class, need_confidence = False):
		self.evaluator_class = evaluator_class
		self.money_total = 0
		self.total_confident_bets = 0
		self.total_bets = 0
		self.bets_won = 0
		self.bets_lost = 0
		self.money_risked = 0
		self.need_confidence = need_confidence
		##array of all matches to bet on
		self.bettable_matches = []
	
	def run(self):
		self.make_bets()

		

	def make_bets(self):
		##populate bettable matches with all matches from db
		cursor = ProMatch.get_bettable_set()
		for m in cursor:
			match = ProMatch.from_dict(m)
			self.bettable_matches.append(match)
		
		self.total_bets = len(self.bettable_matches)
		
		for match in self.bettable_matches: 
			##underdog evaluator takes in different input so need special case
			if self.evaluator_class == UnderdogEvaluator or self.evaluator_class == LoserEvaluator:	
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

				bet_amount = self.calc_bet_amount(team1_ml, team2_ml, winner_predicted)
				self.money_risked += bet_amount
				actual_winner = match.win
				
				
				if(winner_predicted == actual_winner):
					self.bets_won += 1
					if actual_winner == 100:
						if team1_ml >= 100:
							self.money_total += team1_ml
						else:
							self.money_total += bet_amount*100/float(abs(team1_ml))
					elif actual_winner == 200:
						if team2_ml >= 100:
							self.money_total += team2_ml
						else:
							self.money_total += bet_amount*100/float(abs(team2_ml))
				else:
					self.bets_lost += 1
					self.money_total -= bet_amount


	def calc_bet_amount(self, ml1, ml2, winner_predicted):
		bet_amount = 0
		if NORMALIZE_WINNINGS:
			if winner_predicted == 100:
				if ml1 >= 100:
					bet_amount = 100*100/float(ml1)
				elif ml1 < -100:
					bet_amount = abs(ml1)
			else:
				if ml2 >= 100:
					bet_amount = 100*100/float(ml2)
				elif ml2 < -100:
					bet_amount = abs(ml2)
		else:
			bet_amount = 100
		return bet_amount

	def print_results(self):
		print("Total Bets Considered", self.total_bets)
		print("Total Bets Made", self.total_confident_bets)
		print("Money Risked", self.money_risked)
		win_percentage = 100*self.bets_won/float(self.bets_lost + self.bets_won)
		print("Win Percentage", str(win_percentage))
		print("Profit", self.money_total )
		print("")
		print("")
		return (win_percentage, self.money_total)




