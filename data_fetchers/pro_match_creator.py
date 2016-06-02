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

		## LCK WEEK 2
		match_list.append(MatchInfo("LCK, AFs vs Samsung, Week 2", ["Elise","Maokai","Kalista","Twisted Fate","Blitzcrank"]
			, ["Ekko","Nami","Graves","Ashe","Fiora"], 200, "LCK", "6.10"))
		match_list.append(MatchInfo("LCK, Samsung vs AFs, Week 2", ["Viktor","Elise","Nami","Ezreal","Maokai"]
			, ["Lucian","Kindred","Lulu","Braum","Poppy"], 100, "LCK", "6.10"))
		match_list.append(MatchInfo("LCK, ESC vs Jin Air, Week 2", ["Ryze","Kha'Zix","Karma","Tristana","Varus"]
			, ["Lucian","Elise","Azir","Braum","Ekko"], 200, "LCK", "6.10"))
		match_list.append(MatchInfo("LCK, Jin Air vs ESC, Week 2", ["Nidalee","Maokai","Viktor","Sivir","Tahm Kench"]
			, ["Ekko","Ashe","Kindred","Braum","Swain"], 200, "LCK", "6.10"))
		match_list.append(MatchInfo("LCK, ESC vs Jin Air, Week 2", ["Ryze","Ashe","Braum","Rek'Sai","Karma"]
			, ["Viktor","Kindred","Ekko","Sivir","Bard"], 200, "LCK", "6.10"))
		match_list.append(MatchInfo("LCK, LZ vs KT, Week2", ["Rek'Sai","Ekko","Karma","Lucian","Azir"]
		, ["Maokai","Caitlyn","Braum","Elise","Varus"], 100, "LCK", "6.10"))
		match_list.append(MatchInfo("LCK, KT vs LZ, Week2", ["Caitlyn","Elise","Azir","Maokai","Braum"]
		, ["Ekko","Rek'Sai","Viktor","Bard","Jhin"], 100, "LCK", "6.10"))
		match_list.append(MatchInfo("LCK, LZ vs KT, Week2", ["Nidalee","Kalista","Braum","Jayce","Maokai"]
		, ["Ekko","Kindred","Taric","Ezreal","Zilean"], 200, "LCK", "6.10"))
		match_list.append(MatchInfo("LCK, ROX vs MVP, Week2", ["Trundle","Braum","Caitlyn","Varus","Elise"]
		, ["Azir","Rek'Sai","Lucian","Bard","Fizz"], 100, "LCK", "6.10"))
		match_list.append(MatchInfo("LCK, MVP vs ROX, Week2", ["Ekko","Alistar","Varus","Ashe","Amumu"]
		, ["Caitlyn","Rek'Sai","Viktor","Tahm Kench","Rumble"], 100, "LCK", "6.10"))
		match_list.append(MatchInfo("LCK, ROX vs MVP, Week2", ["Trundle","Lucian","Azir","Maokai","Graves"]
		, ["Ekko","Caitlyn","Viktor","Alistar","Rek'Sai"], 100, "LCK", "6.10"))
		##match_list.append(MatchInfo("LCK, S vs F, Week2", ["","","","",""]
		##, ["","","","",""], 200, "LCK", "6.10"))

		## EU CS Group1
		match_list.append(MatchInfo("EUCS, MFT vs Melty, Group A", ["Graves","Trundle","Ezreal","Lissandra","Braum"]
			, ["Ekko","Caitlyn","Morgana","Elise","Zilean"], 100, "EUCS", "6.10"))
		match_list.append(MatchInfo("EUCS, SK vs Tricked, Group A", ["Azir","Elise","Taric","Miss Fortune","Gnar"]
			, ["Braum","Graves","Maokai","Sivir","Vladimir"], 100, "EUCS", "6.10"))
		match_list.append(MatchInfo("EUCS, FNCA vs LP, Group A", ["Trundle","Ezreal","Kindred","Azir","Thresh"]
			, ["Braum","Lucian","Viktor","Gragas","Gnar"], 200, "EUCS", "6.10"))
		match_list.append(MatchInfo("EUCS, MFT vs FNCA, Group A", ["Kindred","Trundle","Lissandra","Ezreal","Maokai"]
			, ["Braum","Lucian","LeBlanc","Graves","Ekko"], 100, "EUCS", "6.10"))
		match_list.append(MatchInfo("EUCS, LP vs Tricked, Group A", ["Ryze","Graves","Trundle","Sivir","Fiora"]
			, ["Ekko","Braum","Gragas","Ezreal","Lissandra"], 100, "EUCS", "6.10"))
		match_list.append(MatchInfo("EUCS, Melty vs SK, Group A", ["Azir","Graves","Maokai","Sivir","Janna"]
			, ["Trundle","Lucian","Gnar","Elise","Viktor"], 200, "EUCS", "6.10"))
		match_list.append(MatchInfo("EUCS, Tricked vs Melty, Group A", ["Graves","Ezreal","Braum","Viktor","Gnar"]
			, ["Trundle","Lucian","Morgana","Elise","LeBlanc"], 100, "EUCS", "6.10"))
		match_list.append(MatchInfo("EUCS, MFT vs LP, Group A", ["Nidalee","Ezreal","Braum","Ekko","LeBlanc"]
			, ["Trundle","Lucian","Karma","Graves","Maokai"], 200, "EUCS", "6.10"))
		match_list.append(MatchInfo("EUCS, FNCA vs SK, Group A", ["Lissandra","Graves","Ezreal","Kennen","Braum"]
			, ["Lucian","Trundle","Viktor","Rek'Sai","Poppy"], 100, "EUCS", "6.10"))
		match_list.append(MatchInfo("EUCS, FNCA vs Tricked, Group A", ["Lissandra","Graves","Alistar","Sivir","Ekko"]
			, ["Trundle","Lucian","Lulu","Nidalee","Ryze"], 200, "EUCS", "6.10"))
		match_list.append(MatchInfo("EUCS, SK vs MFT, Group A", ["Nidalee","Ekko","Azir","Ezreal","Braum"]
			, ["Trundle","Lucian","Vladimir","Graves","Poppy"], 200, "EUCS", "6.10"))
		match_list.append(MatchInfo("EUCS, Melty vs LP, Group A", ["Azir","Kindred","Sivir","Gangplank","Morgana"]
			, ["Lucian","Braum","Viktor","Gragas","Fiora"], 100, "EUCS", "6.10"))
		match_list.append(MatchInfo("EUCS, LP vs SK, Group A", ["Lucian","Graves","Braum","Annie","Gragas"]
			, ["Taric","Nidalee","Twisted Fate","Miss Fortune","Poppy"], 200, "EUCS", "6.10"))
		match_list.append(MatchInfo("EUCS, Melty vs FNCA, Group A", ["Nidalee","Trundle","Sivir","LeBlanc","Morgana"]
			, ["Nami","Lucian","Zed","Lulu","Fiora"], 100, "EUCS", "6.10"))
		match_list.append(MatchInfo("EUCS, Tricked vs MFT, Group A", ["Lucian","Graves","Braum","Lulu","Swain"]
			, ["Trundle","Kindred","Maokai","Sivir","Viktor"], 200, "EUCS", "6.10"))
		
		##EUCS Group B
		match_list.append(MatchInfo("EUCS, Kick vs S6, Group B", ["Nidalee","Poppy","Caitlyn","Syndra","Janna"]
		, ["Maokai","Kindred","LeBlanc","Ezreal","Nami"], 100, "EUCS", "6.10"))
		match_list.append(MatchInfo("EUCS, Forge vs ESG, Group B", ["Trundle","Lucian","Elise","Morgana","Bard"]
		, ["Alistar","Graves","Viktor","Ezreal","Swain"], 100, "EUCS", "6.10"))
		match_list.append(MatchInfo("EUCS, Mouz vs G2V, Group B", ["Trundle","Sivir","Alistar","Elise","LeBlanc"]
		, ["Gragas","Kalista","Viktor","Braum","Gnar"], 100, "EUCS", "6.10"))
		match_list.append(MatchInfo("EUCS, Kick vs mouz, Group B", ["Braum","Elise","Ezreal","Poppy","Viktor"]
		, ["Ekko","Sivir","Alistar","Rek'Sai","Fizz"], 100, "EUCS", "6.10"))
		match_list.append(MatchInfo("EUCS, G2V vs ESG, Group B", ["Lucian","Bard","Lissandra","Gnar","Graves"]
		, ["Trundle","Kindred","Janna","Caitlyn","Viktor"], 100, "EUCS", "6.10"))
		match_list.append(MatchInfo("EUCS, S6 vs Forge, Group B", ["Lucian","Maokai","Janna","Gragas","Quinn"]
		, ["Braum","Elise","Lissandra","Draven","Lulu"], 100, "EUCS", "6.10"))
		match_list.append(MatchInfo("EUCS, ESG vs S6, Group B", ["Kindred","Braum","Viktor","Sivir","Gnar"]
		, ["Lucian","Graves","Zilean","Maokai","Janna"], 100, "EUCS", "6.10"))
		match_list.append(MatchInfo("EUCS, Kick vs G2V, Group B", ["Braum","Caitlyn","Viktor","Poppy","Gragas"]
		, ["Trundle","Nidalee","Ryze","Kalista","Thresh"], 100, "EUCS", "6.10"))
		match_list.append(MatchInfo("EUCS, mouz vs Forge, Group B", ["Maokai","Braum","Viktor","Kalista","Nunu"]
		, ["Kindred","Alistar","Ekko","Sivir","Morgana"], 200, "EUCS", "6.10"))
		match_list.append(MatchInfo("EUCS, mouz vs ESG, Group B", ["Trundle","Ezreal","Braum","Elise","Aurelion Sol"]
		, ["Lissandra","Kindred","Bard","Caitlyn","Maokai"], 200, "EUCS", "6.10"))
		match_list.append(MatchInfo("EUCS, Forge vs Kick, Group B", ["Trundle","Ekko","Sivir","Vladimir","Alistar"]
		, ["Viktor","Braum","Poppy","Ezreal","Kindred"], 100, "EUCS", "6.10"))
		match_list.append(MatchInfo("EUCS, S6 vs G2V, Group B", ["Nidalee","Braum","Ryze","Caitlyn","Poppy"]
		, ["Alistar","Sivir","Lissandra","Fizz","Gnar"], 100, "EUCS", "6.10"))
		match_list.append(MatchInfo("EUCS, G2V vs Forge, Group B", ["Kindred","Janna","Caitlyn","LeBlanc","Irelia"]
		, ["Trundle","Lucian","Ekko","Viktor","Alistar"], 100, "EUCS", "6.10"))
		match_list.append(MatchInfo("EUCS, S6 vs mouz, Group B", ["Kindred","Caitlyn","Braum","Maokai","LeBlanc"]
		, ["Alistar","Ekko","Elise","Ezreal","Viktor"], 200, "EUCS", "6.10"))
		match_list.append(MatchInfo("EUCS, ESG vs Kick, Group B", ["Kindred","Ezreal","Karma","Gnar","Alistar"]
		, ["Trundle","Sivir","Gragas","Braum","LeBlanc"], 100, "EUCS", "6.10"))
		## EUCS Finals
		match_list.append(MatchInfo("EUCS, MFT vs ESG, Finals", ["Lucian","Rek'Sai","Ekko","Kassadin","Bard"]
		, ["Braum","Vladimir","Graves","Sivir","Gnar"], 100, "EUCS", "6.10"))
		match_list.append(MatchInfo("EUCS, ESG vs MFT, Finals", ["Lucian","Rek'Sai","Braum","Gnar","Azir"]
		, ["Viktor","Trundle","Maokai","Sivir","Graves"], 100, "EUCS", "6.10"))
		match_list.append(MatchInfo("EUCS, MFT vs ESG, Finals", ["Azir","Caitlyn","Trundle","Elise","Braum"]
		, ["Ekko","Rek'Sai","Bard","Ezreal","Gnar"], 100, "EUCS", "6.10"))
		match_list.append(MatchInfo("EUCS, ESG vs MFT, Finals", ["Kindred","Sivir","Bard","Ekko","Karma"]
		, ["Viktor","Caitlyn","Elise","Braum","Trundle"], 200, "EUCS", "6.10"))
		match_list.append(MatchInfo("EUCS, Forge vs SK, Finals", ["Ryze","Elise","Braum","Draven","Poppy"]
		, ["Trundle","Viktor","Graves","Sivir","Maokai"], 100, "EUCS", "6.10"))
		match_list.append(MatchInfo("EUCS, SK vs Forge, Finals", ["Viktor","Morgana","Caitlyn","Ekko","Rek'Sai"]
		, ["Lucian","Elise","Karma","Alistar","Poppy"], 200, "EUCS", "6.10"))
		match_list.append(MatchInfo("EUCS, Forge vs SK, Finals", ["Elise","Jhin","Trundle","Morgana","Poppy"]
		, ["Viktor","Sivir","Taric","Kindred","Fiora"], 200, "EUCS", "6.10"))
		match_list.append(MatchInfo("EUCS, SK vs Forge, Finals", ["Ryze","Taric","Miss Fortune","Gragas","Poppy"]
		, ["Sivir","Kindred","Viktor","Braum","Maokai"], 200, "EUCS", "6.10"))
		
		##NACS Qualifier
		match_list.append(MatchInfo("NACS, C9C vs DFGL, Qualifier", ["Kindred","Sivir","Braum","Maokai","Gangplank"]
		, ["Ezreal","Ekko","Veigar","Elise","Trundle"], 100, "NACS", "6.10"))
		match_list.append(MatchInfo("NACS, C9C vs DFGL , Qualifier", ["Ryze","Lee Sin","Ezreal","Ekko","Braum"]
		, ["Trundle","Maokai","Gragas","Caitlyn","Viktor"], 100, "NACS", "6.10"))
		match_list.append(MatchInfo("NACS, C9C vs DFGL, Qualifier", ["Kindred","Ekko","Ezreal","Gangplank","Zyra"]
		, ["Lee Sin","Braum","Jhin","Rumble","Zed"], 100, "NACS", "6.10"))
		match_list.append(MatchInfo("NACS, ASN vs dT , Qualifier", ["Maokai","Azir","Braum","Rek'Sai","Ezreal"]
		, ["Kindred","Lucian","Trundle","Zilean","Alistar"], 200, "NACS", "6.10"))
		match_list.append(MatchInfo("NACS, ASN vs dT , Qualifier", ["Maokai","Azir","Kindred","Trundle","Sivir"]
		, ["Lucian","Braum","Gragas","Zilean","Gangplank"], 200, "NACS", "6.10"))
		match_list.append(MatchInfo("NACS, ASN vs dT, Qualifier", ["Ekko","Azir","Elise","Thresh","Miss Fortune"]
			, ["Kindred","Braum","Zilean","Maokai","Sivir"], 200, "NACS", "6.10"))
		##match_list.append(MatchInfo("NACS, S vs , Qualifier", ["","","","",""]
		##, ["","","","",""], 200, "NACS", "6.10"))
		return match_list
		
