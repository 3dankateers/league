############################################################################
## analyzes training data matches and trains a decison kneighbours model
############################################################################
from sklearn.neighbors import KNeighborsClassifier
from match_hyperpoint import MatchHyperpoint
import numpy as np
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

class KNeighboursCalculator:

	##static member stores neigh model so recalculation is not neccesary every time it is used
	neigh_model = None

	def __init__(self):
		pass	
	
	@staticmethod
	def get_neigh_model():
		if KNeighboursCalculator.neigh_model == None:
			KNeighboursCalculator.neigh_model = KNeighboursCalculator.get_new_model()
		return KNeighboursCalculator.neigh_model
	
	##returns neigh model
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
		new_neigh_model = KNeighborsClassifier(n_neighbors = 4, weights = "uniform", algorithm = "ball_tree", p = 2)
		new_neigh_model.fit(X,y)
		print "New K-Neighbours model created: "
		KNeighboursCalculator.neigh_model = new_neigh_model
		return new_neigh_model
