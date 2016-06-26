## Handles retraining
## Separates training set from test set

from match import Match
from pro_match import ProMatch
from champ_winrate_calculator import ChampWinrateCalculator
from pair_winrate_calculator import PairWinrateCalculator
from hyperpoint_calculator import HyperpointCalculator
from random import randint


## out of how many matches should a test be set
## num_total_tests = ( 1/NUM_TESTS * num_total_matches)
NUM_TESTS = 10
NUM_PRO_TESTS = 5

class Trainer():
	
	##type constants that signify what to train on
	SOLOQ = "soloq"
	PRO_MATCHES = "pro_matches"
	PREMADE = "premade"

	## type constants for what training is needed
	ONE_CHAMP = "one_champ"
	PAIR = "pair"
	HYPERPOINTS = "hyperpoints"
	ALL = "all"
	NONE = "none"

	@staticmethod
	def set_new_soloq_tests():
		##before assigning new tests, remove all previous ones
		Match.reset_all_tests(is_test = False)
		
		##used to decide which matches are set as tests	
		rand = randint(0,NUM_TESTS)
		
		cursor = Match.get_testable_set()
		num_matches = cursor.count()

		for i in range(num_matches):
			match = Match.from_dict(cursor[i])

			## set match as test
			if  i%NUM_TESTS == rand:
				match.is_test = True
				match.save()
	
	##set is_test for matches only if both sides of the match are a premade team
	@staticmethod
	def set_premade_tests():
		Match.reset_all_tests(is_test = False)
		cursor = Match.get_testable_set()
		for m in cursor:
			match = Match.from_dict(m)
			if match.isTeam1 and match.isTeam2:
				match.is_test = True
				match.save()

	@staticmethod
	def set_promatch_training_set():
		##remove all tests
		ProMatch.reset_all_tests(is_test = False)
		
		##used to decide which matches are set as tests	
		rand = randint(0,NUM_PRO_TESTS)
		
		cursor = ProMatch.get_testable_set()
		num_matches = cursor.count()

		for i in range(num_matches):
			match = ProMatch.from_dict(cursor[i])

			## set match as test
			if  i%NUM_TESTS == rand:
				##num_tests+= 1
				match.is_test = True
				match.save()

	##passed in training set type to train from
	##passed in data_type_needed to train
	
	@staticmethod
	def train(train_set_type, data_type_needed):
		if train_set_type == Trainer.SOLOQ:
			print "here"
			##ProMatch.reset_all_tests(is_test = True)
			##Trainer.set_new_soloq_tests()
			match_class = Match
		elif train_set_type == Trainer.PREMADE:
			ProMatch.reset_all_tests(is_test = True)
			Trainer.set_premade_tests()
			match_class = Match
		elif train_set_type == Trainer.PRO_MATCHES:
			##Match.reset_all_tests(is_test = True)
			Trainer.set_promatch_training_set()
			match_class = ProMatch
		
		if data_type_needed == Trainer.ALL:
			print "Training all"
			champ_calculator = ChampWinrateCalculator(match_class, "win")
			champ_calculator.run()
			pair_calculator = PairWinrateCalculator(match_class, "win")
			pair_calculator.run()
			hyperpoint_calculator = HyperpointCalculator(match_class, "win")
			hyperpoint_calculator.run()
		elif data_type_needed == Trainer.ONE_CHAMP:
			print "Training One Champ"
			champ_calculator = ChampWinrateCalculator(match_class, "win")
			champ_calculator.run()
		elif data_type_needed == Trainer.PAIR:
			print "Training Pair"
			pair_calculator = PairWinrateCalculator(match_class, "win")
			pair_calculator.run()
		elif data_type_needed == Trainer.HYPERPOINTS:
			print "Training Hyperpoints"
			hyperpoint_calculator = HyperpointCalculator(match_class, "win")
			hyperpoint_calculator.run()
		elif data_type_needed == Trainer.NONE:
			print "No Training Needed"

