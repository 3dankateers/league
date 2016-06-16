## for now use this to manually add pro_matches

from pro_match import ProMatch
from champ import Champ
import StringIO
import csv

## store intermediate match_info
class MatchInfo:
	def __init__(self, description, champs1_names, champs2_names, win, region, patch):
		self.description = description
		self.champs1_names = champs1_names
		self.champs2_names = champs2_names
		self.win = win
		self.region = region
		self.patch = patch

## checks that champions are spelled properly
def champ_names_to_ids(champ_names):
	team_ids = []
	for champ_name in champ_names:
		cursor = Champ.find_champ_by_name(champ_name)
		if cursor.count() == 0:
			print "Mistyped champ name: ", champ_name
		champ = Champ.from_dict(cursor[0])
		team_ids.append(champ.id)
	return team_ids


## csv label column:
## ['team1_name', 'team2_name', 'map_number', 'champs1_names', 'champs2_names', 'win', 'match_day', 'first_blood', 'kills_5']

class ProMatchCreator:
	
	def run(self):
		self.add_matches("EU_LCS_WEEK2.csv")
		self.add_matches("NA_LCS_WEEK2.csv")
		self.add_matches("LCK_WEEK3.csv")
		self.add_matches("LCK_WEEK4.csv")
		self.add_matches("NACS_WEEK2.csv")
		self.add_matches("LPL_WEEK3.csv")
		self.add_matches("LSPL_6.11.csv")

	##adds pro matches to db (may contain duplicates)
	def add_matches(self, file):
		##Possibly populated later by csv file: 				champs1, champs2, win, first_blood, kills_5, status
		with open("C:/Users/andrei/dev/league/csv_data/" + file, 'r') as csvfile:
			contents = csv.reader(csvfile)
			label_row = []
			for i, row in enumerate(contents):
				if i == 0:
					label_row = row
				
				else:
					params_dict = ProMatchCreator.parse_row_params(label_row, row)
					
					if params_dict['map_number'] == None:
						continue

					team1_name = params_dict['team1_name']
					team2_name = params_dict['team2_name']
					map_number = int(params_dict['map_number'])
					match_day = params_dict['match_day']
					## if already exists this gets existing match, otherwise create new match with those parameters
					match = ProMatch.find_match(team1_name, team2_name, map_number, match_day, "csv")
					
					##if match already created and status is nitrogen update to "both", else status = "csv"
					
					##don't update match if both already since it will cause inversion problems
					if match.status != "both":
						if match.status == "nitrogen":
							match.status = "both"
							print "Nitrogen promatch updated"
						elif match.status == None:
							match.status = "csv"
							print "New csv promatch created"
						
						match.champs1 = ProMatchCreator.champs_string_to_ids(params_dict['champs1_names'])
						match.champs2 = ProMatchCreator.champs_string_to_ids(params_dict['champs2_names'])
						match.win = int(params_dict['win'])
						if params_dict["first_blood"] != None:
							match.first_blood = int(params_dict['first_blood'])
						if params_dict["kills_5"] != None:
							match.kills_5 = int(params_dict['kills_5'])
						match.is_test = True
						##red side should always be first team(100) in csv file 
						## this is why inversion is neccesary since nitrogen lists alphabetically(doesn't care about sides)
						match.red_side = 100
						## match.save will do inversion if neccesary
						match.save()
		
		csvfile.close()

	##takes in a string containing champ names
	## returns array of corresponding champ ids
	@staticmethod
	def champs_string_to_ids(champ_string):
		champ_names = champ_string.split(", ")
		return champ_names_to_ids(champ_names)


	##takes in label_row(contains column names) and a row and returns the data organized into a dict
	@staticmethod
	def parse_row_params(label_row, params_row):
		param_dict = {}
		for i, col_name in enumerate(label_row):
			##set to None if column value not set(for first blood, kills_5 which are not required)
			if params_row[i] == '':
				param_dict[col_name] = None
			else:
				param_dict[col_name] = params_row[i]
		return param_dict
			
		
