from db_client import DbClient
from Match import match
from random import randint

## out of how many matches should a test be set
## num_total_tests = ( 1/NUM_TESTS * num_total_matches)
NUM_TESTS = 10

class Test:

	@staticmethod
	def set_new_tests():
		##used to decide which matches are set as tests	
		rand = randint(0,NUM_TESTS)
		
		cursor = Match.get_all_matches()
		num_matches = cursor.count()

		for i in range(num_matches):
			match = Match.from_dict(cursor[i])
			
			## set match as test
			if  i%rand == 0:
				match.is_test = True
				match.save()
			##match is not test
			else match.is_test == True:
				match.is_test = False
				match.save()



