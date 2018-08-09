## small class used to find better parameters for svm

from svm_evaluator import SVMEvaluator
from cross_validator import CrossValidator

class SVMTrainer:
	
	@staticmethod
	def run():
		C_vals = [0.125]
		gamma_vals = [0.0005, 0.001, 0.002]

		for C_val in C_vals:
			for gamma_val in gamma_vals:
				SVMEvaluator.retrain(C_val, gamma_val)
				cv = CrossValidator(SVMEvaluator, 1)
				cv.run()
				print("C = ", C_val, " gamma = ", gamma_val)
				cv.print_results()

