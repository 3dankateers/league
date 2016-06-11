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
	##adds pro matches to db (may contain duplicates)
	def add_matches(self):
		##Possibly populated later by csv file: 				champs1, champs2, win, first_blood, kills_5, status
		with open("C:/Users/andrei/dev/league/csv_data/EU_LCS_WEEK2.csv", 'r') as csvfile:
			contents = csv.reader(csvfile)
			label_row = []
			for i, row in enumerate(contents):
				if i == 0:
					label_row = row
				else:
					params_dict = ProMatchCreator.parse_row_params(label_row, row)
					team1_name = params_dict['team1_name']
					team2_name = params_dict['team2_name']
					map_number = params_dict['map_number']
					match_day = params_dict['match_day']
					## if already exists this gets existing match, otherwise create new match with those parameters
					match = ProMatch.find_match(team1_name, team2_name, map_number, match_day)
					
					##if match already created and status is nitrogen update to "both", else status = "csv"
					if match.status == "nitrogen":
						match.status = "both"
						print "Nitrogen promatch updated"
					elif match.status == None:
						match.status = "csv"
						print "New csv promatch created"
					
					match.champs1 = ProMatchCreator.champs_string_to_ids(params_dict['champs1_names'])
					match.champs2 = ProMatchCreator.champs_string_to_ids(params_dict['champs2_names'])
					match.win = int(params_dict['win'])
					match.first_blood = params_dict['first_blood']
					match.kills_5 = params_dict['kills_5']
					match.save()
		
		csvfile.close()

	##takes in a string containing champ names
	## returns array of corresponding champ ids
	@staticmethod
	def champs_string_to_ids(champ_string):
		champ_names = champ_string.split(", ")
		print champ_names
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
			
		
