## for now use this to manually add pro_matches

from pro_match import ProMatch
from champ import Champ

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
		matches_to_add = self.input_matches()
		for m in matches_to_add:
			champ1_ids = champ_names_to_ids(m.champs1_names)
			champ2_ids = champ_names_to_ids(m.champs2_names)
			pm = ProMatch(m.description, champ1_ids, champ2_ids, m.win, m.region, m.patch, is_test = True)
			pm.save()

	
	## add matches manually here
	def input_matches(self):
		match_list = []
		
		##LCK WEEK1
		match_list.append(MatchInfo("LCK, AFs vs LZ, Week 1", ["Ekko", "Rek'Sai", "Caitlyn", "Fizz", "Bard"]
			, ["Azir", "Alistar", "Elise", "Maokai", "Ezreal"], 100, "LCK", "6.10"))
		match_list.append(MatchInfo("LCK, LZ vs AFs, Week 1", ["Lucian", "Elise", "Ekko", "Azir", "Nami"]
			, ["Maokai", "Karma", "Lee Sin", "Sivir", "Viktor"], 200, "LCK", "6.10"))
		match_list.append(MatchInfo("LCK, CJ vs ESC, Week 1", ["Kindred", "Maokai", "Braum", "Ezreal", "Viktor"]
			, ["Ekko", "Azir", "Nidalee", "Ashe", "Bard"], 200, "LCK", "6.10"))
		match_list.append(MatchInfo("LCK, ESC vs CJ, Week 1", ["Ryze","Elise","Varus","Caitlyn","Bard"]
			, ["Lucian","Rek'Sai","Veigar","Maokai","Thresh"], 100, "LCK", "6.10"))
		match_list.append(MatchInfo("LCK, ROXT vs Samsung, Week 1", ["Ekko","Ezreal","Aurelion Sol","Swain","Alistar"]
			, ["Viktor","Lucian","Rek'Sai","Maokai","Nami"], 200, "LCK", "6.10"))
		match_list.append(MatchInfo("LCK, Samsung vs ROXT, Week 1", ["Nidalee","Soraka","Ezreal","Varus","Poppy"]
			, ["Azir","Lucian","Fizz","Bard","Elise"], 100, "LCK", "6.10"))
		match_list.append(MatchInfo("LCK, MVP vs KT, Week 1", ["Lucian","Braum","Maokai","Twitch","Elise"]
			, ["Viktor","Rek'Sai","Ekko","Sivir","Taric"], 200, "LCK", "6.10"))
		match_list.append(MatchInfo("LCK, KT vs MVP, Week 1", ["Kindred","Sivir","Viktor","Swain","Bard"]
			, ["Maokai","Elise","Azir","Caitlyn","Karma"], 100, "LCK", "6.10"))
		match_list.append(MatchInfo("LCK, Jin Air vs LZ, Week 1", ["Rek'Sai","Maokai","Sivir","Azir","Karma"]
			, ["Ekko","Viktor","Bard","Graves","Caitlyn"], 100, "LCK", "6.10"))
		match_list.append(MatchInfo("LCK, LZ vs Jin Anir, Week 1", ["Viktor","Graves","Ekko","Ezreal","Braum"]
			, ["Rek'Sai","Lucian","Maokai","Twisted Fate","Zyra"], 200, "LCK", "6.10"))
		
		
		##LPL WEEK1
		match_list.append(MatchInfo("LPL, EDG vs Newbee, Week 1", ["Trundle","Rek'Sai","Karma","Caitlyn","Azir"]
			, ["Lucian","Braum","Lee Sin","Swain","Viktor"], 100, "LPL", "6.10"))
		match_list.append(MatchInfo("LPL, Newbee vs EDG, Week 1", ["Lucian","Trundle","Graves","Kassadin","Bard"]
			, ["Maokai","Viktor","Evelynn","Caitlyn","Braum"], 100, "LPL", "6.10"))
		match_list.append(MatchInfo("LPL, EDG vs Newbee, Week 1", ["Kindred","Alistar","Viktor","Kalista","Fizz"]
			, ["Ekko","Lucian","Rek'Sai","Bard","Veigar"], 100, "LPL", "6.10"))
		match_list.append(MatchInfo("LPL, Snake vs GMT, Week 1", ["Rek'Sai","Twitch","Karma","Fizz","Lissandra"]
			, ["Viktor","Maokai","Bard","Ezreal","Graves"], 100, "LPL", "6.10"))
		match_list.append(MatchInfo("LPL, GMT vs Snake, Week 1", ["Rek'Sai","Karma","Twitch","Ekko","Viktor"]
			, ["Maokai","Azir","Bard","Elise","Tristana"], 100, "LPL", "6.10"))
		match_list.append(MatchInfo("LPL, Snake vs GMT, Week 1", ["Lucian","Viktor","Maokai","Elise","Braum"]
			, ["Karma","Rek'Sai","Ekko","Ezreal","Kassadin"], 200, "LPL", "6.10"))
		match_list.append(MatchInfo("LPL, RNG vs WE, Week 1", ["Maokai","Alistar","Viktor","Ezreal","Graves"]
			, ["Sivir","Rek'Sai","Nautilus","Bard","Azir"], 200, "LPL", "6.10"))
		match_list.append(MatchInfo("LPL, WE vs RNG, Week 1", ["Rek'Sai","Braum","Nautilus","Twitch","Viktor"]
			, ["Maokai","Sivir","Elise","Karma","Swain"], 200, "LPL", "6.10"))
		match_list.append(MatchInfo("LPL, RNG vs WE, Week 1", ["Kindred","Trundle","Viktor","Ezreal","Thresh"]
			, ["Ekko","Caitlyn","Nidalee","Karma","Kassadin"], 100, "LPL", "6.10"))
		match_list.append(MatchInfo("LPL, OMG vs IMAY, Week 1", ["Ryze","Thresh","Maokai","Jhin","Graves"]
			, ["Sivir","Rek'Sai","Viktor","Bard","Ekko"], 200, "LPL", "6.10"))
		match_list.append(MatchInfo("LPL, IMAY vs OMG, Week 1", ["Trundle","Graves","Viktor","Caitlyn","Tahm Kench"]
			, ["Maokai","Sivir","Twisted Fate","Elise","Karma"], 100, "LPL", "6.10"))
		match_list.append(MatchInfo("LPL, EDG vs Snake, Week 1", ["Kindred","Maokai","Braum","Ashe","Viktor"]
			, ["Lucian","Karma","Ekko","Rek'Sai","Azir"], 100, "LPL", "6.10"))
		match_list.append(MatchInfo("LPL, Snake vs EDG, Week 1", ["Ekko","Elise","Karma","Sivir","Alistar"]
			, ["Lucian","Rek'Sai","Fizz","Braum","Azir"], 200, "LPL", "6.10"))
		match_list.append(MatchInfo("LPL, GMT vs Saint, Week 1", ["Kindred","Ekko","Azir","Ezreal","Trundle"]
			, ["Lucian","Viktor","Elise","Swain","Thresh"], 100, "LPL", "6.10"))
		match_list.append(MatchInfo("LPL, Saint vs GMT, Week 1", ["Twitch","Elise","Ekko","Kassadin","Janna"]
			, ["Karma","Azir","Lee Sin","Fizz","Sivir"], 200, "LPL", "6.10"))
		match_list.append(MatchInfo("LPL, Newbee vs IG, Week 1", ["Kindred","Trundle","Ezreal","Twisted Fate","Bard"]
			, ["Caitlyn","Maokai","Graves","Braum","Lissandra"], 100, "LPL", "6.10"))
		match_list.append(MatchInfo("LPL, IG vs Newbee, Week 1", ["Nidalee","Sivir","Bard","Twisted Fate","Fiora"]
			, ["Maokai","Karma","Kindred","Lucian","Fizz"], 100, "LPL", "6.10"))
		match_list.append(MatchInfo("LPL, Newbee vs IG, Week 1", ["Kindred","Bard","Sivir","Kassadin","Swain"]
			, ["Viktor","Maokai","Karma","Lucian","Rek'Sai"], 100, "LPL", "6.10"))
		match_list.append(MatchInfo("LPL, LGD vs IMAY, Week 1", ["Viktor","Elise","Lucian","Trundle","Alistar"]
			, ["Rek'Sai","Sivir","Ekko","Nautilus","LeBlanc"], 200, "LPL", "6.10"))
		match_list.append(MatchInfo("LPL, IMAY vs LGD, Week 1", ["Rek'Sai","Sivir","Ekko","Zilean","Bard"]
			, ["Viktor","Kindred","Twitch","Maokai","Thresh"], 100, "LPL", "6.10"))
		match_list.append(MatchInfo("LPL, RNG vs VG, Week 1", ["Kindred","Swain","Alistar","Caitlyn","Viktor"]
			, ["Azir","Graves","Karma","Ezreal","Kha'Zix"], 100, "LPL", "6.10"))
		match_list.append(MatchInfo("LPL, VG vs RNG, Week 1", ["Lucian","Ekko","Azir","Graves","Thresh"]
			, ["Bard","Rek'Sai","Viktor","Maokai","Caitlyn"], 200, "LPL", "6.10"))
		match_list.append(MatchInfo("LPL, WE vs OMG, Week 1", ["Lucian","Maokai","Trundle","Viktor","Graves"]
			, ["Bard","Rek'Sai","Fizz","Caitlyn","LeBlanc"], 100, "LPL", "6.10"))
		match_list.append(MatchInfo("LPL, OMG vs WE, Week 1", ["Kindred","Ekko","Bard","Jhin","Lissandra"]
			, ["Maokai","Lucian","Twisted Fate","Braum","Rek'Sai"], 200, "LPL", "6.10"))
		##match_list.append(MatchInfo("LPL, CJ vs ESC, Week 1", ["","","","",""]
		##	, ["","","","",""], 200, "LPL", "6.10"))
		return match_list
		
