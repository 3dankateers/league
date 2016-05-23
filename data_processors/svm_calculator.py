############################################################################
## analyzes training data matches and calculates winrates a svm model
############################################################################
from sklearn import svm
from sklearn.utils import check_X_y, check_array
from match_hyperpoint import MatchHyperpoint
import numpy as np
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

class SVMCalculator:

	##static member stores svm model so recalculation is not neccesary every time it is used
	svm_model = None

	def __init__(self):
		pass	
	
	@staticmethod
	def get_svm_model():
		if SVMCalculator.svm_model == None:
			SVMCalculator.svm_model = SVMCalculator.train_model()
		return SVMCalculator.svm_model
	
	##returns svm model
	@staticmethod
	def train_model():
		X = []
		y = []

		cursor = MatchHyperpoint.get_all()

		for h in cursor:
			mh = MatchHyperpoint.from_dict(h)
			X.append(mh.coordinates)
			y.append(mh.winner)
		
		X = np.array(X)
		y = np.array(y)
		##print str(X.size)
		##print str(X.size)
		##print str(X.shape)
		
		##X = np.array(X).reshape(1,(len(X)))
		##y = np.array(y).

		svm_model = svm.SVC(kernel = "rbf", C = 1, gamma = 1/float(10), decision_function_shape = "ovr",  verbose = True)
		svm_model.fit(X,y)
		print "New SVM model created: "
		print str(svm_model)
		print str(svm_model.decision_function)
		return svm_model



