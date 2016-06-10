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

class ProMatchCreator:

	##adds pro matches to db (may contain duplicates)
	def add_matches(self):
		with open('/csv_data/EU_LCS_WEEK2.csv', 'rb') as csvfile:
			contents = csv.reader(csvfile)
			print contents
		matches_to_add = self.input_matches()
		for m in matches_to_add:
			champ1_ids = champ_names_to_ids(m.champs1_names)
			champ2_ids = champ_names_to_ids(m.champs2_names)
			pm = ProMatch(m.description, champ1_ids, champ2_ids, m.win, m.region, m.patch, is_test = True)
			pm.save()

	
	## add matches manually here
	def input_matches(self):
		
