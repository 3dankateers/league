############################################################################
## analyzes training data matches and trains a decison tree model
############################################################################
from sklearn import tree
from sklearn.utils import check_X_y, check_array
from match_hyperpoint import MatchHyperpoint
import numpy as np
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

class TreeCalculator:

	##static member stores tree model so recalculation is not neccesary every time it is used
	tree_model = None

	def __init__(self):
		pass	
	
	@staticmethod
	def get_tree_model():
		if TreeCalculator.tree_model == None:
			TreeCalculator.tree_model = TreeCalculator.get_new_model()
		return TreeCalculator.tree_model
	
	##returns tree model
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
		new_tree_model = tree.DecisionTreeClassifier(max_features = 3, criterion = "gini", max_depth = 20, min_samples_leaf = 3)
		new_tree_model.fit(X,y)
		print("New Decision Tree model created: ")
		TreeCalculator.tree_model = new_tree_model
		return new_tree_model
