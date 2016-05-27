############################################################################
## Calculate house edge based on 2 ML odds
############################################################################

class EdgeCalculator:
	
	## print information about 2 ML odds given
	@staticmethod
	def analyze_odds(ml1, ml2):
		print "ML1:", str(ml1)
		print "ML2:", str(ml2)
		implied_p1 = EdgeCalculator.ml_to_prob(ml1)
		implied_p2 = EdgeCalculator.ml_to_prob(ml2)
		print "implied probability1 = ", str(implied_p1)	
		print "implied probability2 = ", str(implied_p2)
		normal_p1 = implied_p1/(implied_p1 + implied_p2)
		normal_p2 = implied_p2/(implied_p1 + implied_p2)
		print "actual probability1 = ", str(normal_p1)	
		print "actual probability2 = ", str(normal_p2)
		print "loss spread = ", str(implied_p1 + implied_p2 - 1)


	
	@staticmethod
	def ml_to_prob(ml):
		prob = 0
		if(ml < 0):
			prob = -1*(ml)/float(100-ml) 
		else:
			prob = 100/float(ml+100)
		return prob
	
	@staticmethod
	def prob_to_ml(prob):
		ml = 0
		if(prob < 0.5):
			ml = 100*(prob)/(prob - 1)
		else:
			ml = (100-100*(prob))/prob
		return ml
