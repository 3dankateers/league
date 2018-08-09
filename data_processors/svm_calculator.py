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
			SVMCalculator.svm_model = SVMCalculator.get_new_model()
		return SVMCalculator.svm_model
	
	##returns svm model
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
		##C=0.5 gamma = 0.05 => 58%
		new_svm_model = svm.LinearSVC(C = 1,  class_weight = 'balanced')
		##new_svm_model = svm.LinearSVC(kernel = "linear", C = 0.5, degree = 1, probability = True, gamma = 0.01, decision_function_shape = "ovr",  verbose = False)
		##svm_model = svm.SVC(kernel = "poly", C = 1, degree = 3, gamma = 0.05, decision_function_shape = "ovr",  verbose = True)
		new_svm_model.fit(X,y)
		print("New SVM model created: ")
		##print str(new_svm_model)
		##print str(new_svm_model.n_support_)
		##print str(new_svm_model.decision_function)
		SVMCalculator.svm_model = new_svm_model
		return new_svm_model



