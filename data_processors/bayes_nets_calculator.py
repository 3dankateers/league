############################################################################
## analyzes training data matches and trains a bayes nets model
############################################################################
from sklearn.naive_bayes import GaussianNB
from sklearn.utils import check_X_y, check_array
from match_hyperpoint import MatchHyperpoint
import numpy as np
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

class BayesNetsCalculator:

	##static member stores bayes nets model so recalculation is not neccesary every time it is used
	bayes_nets_model = None

	def __init__(self):
		pass	
	
	@staticmethod
	def get_bayes_nets_model():
		if BayesNetsCalculator.bayes_nets_model == None:
			BayesNetsCalculator.bayes_nets_model = BayesNetsCalculator.get_new_model()
		return BayesNetsCalculator.bayes_nets_model
	
	##returns bayes nets model
	@staticmethod
	def get_new_model():
		X = []
		y = []

		cursor = MatchHyperpoint.get_all()
		for h in cursor:
			mh = MatchHyperpoint.from_dict(h)
			X.append(mh.coordinates)
			y.append(mh.winner)
		
		X = np.array(X)
		y = np.array(y)
		new_bayes_nets_model = GaussianNB() 
		new_bayes_nets_model.fit(X,y)
		print("New Bayes Nets model created: ")
		BayesNetsCalculator.bayes_nets_model = new_bayes_nets_model
		return new_bayes_nets_model
