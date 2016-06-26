##Note only works with ProMatches that have betting data, should only be called by simulate bets class
##Evaluator return underdog as predicted winner

from evaluator import Evaluator

class UnderdogEvaluator(Evaluator):

	## corresponds to difference in MLs
	CONFIDENT_THRESHOLD = 100
	
	def __init__(self, match):
		self.match = match
		self.ml1 = match.get_latest_ML_T1()
		self.ml2 = match.get_latest_ML_T2()

	## return 100 if team1 is favoured, else return 200
	def predict_winner(self):
		return self.winner
	
	##no training is neccesary for this evaluator
	@staticmethod
	def retrain(prediction_target, premade_only):
		pass

	##return true if confident in predicted winner, otherwise false
	def is_confident(self):
		if abs(self.ml1 - self.ml2) > CONF_THRESHOLD:
			return True
		else:
			return False

	## figure out who is the underdog and return
	def process(self):
		if self.ml1 < 0 and self.ml2 < 0:
			if self.ml1 <= self.ml2:
				self.winner = 200
			else:
				self.winner = 100
		##negative ml means not underdog
		elif self.ml1 < 0:
			self.winner = 200
		else:
			self.winner = 100

	## nothing to print
	def print_results(self):
		pass
	
	@staticmethod
	def print_class():
		print "Underdog Evaluator"
