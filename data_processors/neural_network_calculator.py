############################################################################
## analyzes training data matches and trains a neural network model
############################################################################
from sklearn.neural_network import MLPClassifier
from match_hyperpoint import MatchHyperpoint
import numpy as np
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

class NeuralNetworkCalculator:

	##static member stores neural model so recalculation is not neccesary every time it is used
	neural_model = None

	def __init__(self):
		pass	
	
	@staticmethod
	def get_neural_model():
		if NeuralNetworkCalculator.neural_model == None:
			NeuralNetworkCalculator.neural_model = NeuralNetworkCalculator.get_new_model()
		return NeuralNetworkCalculator.neural_model
	
	##returns neural model
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
		new_neural_model = MLPClassifier()
		new_neural_model.fit(X,y)
		print "New neural netowrk model created: "
		NeuralNetworkCalculator.neural_model = new_neural_model
		return new_neural_model
