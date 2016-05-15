########################################################################
## parses data from league_client
## inserts all champs into db
########################################################################
from champ import Champ

class ChampParser:
	
	## insert each champ in db
	@staticmethod
	def populate_champ_db(lc):
		champ_data = lc.get_champ_data()
		champ_dict = champ_data["data"]
		for key, value in champ_dict.iteritems():
			id = value["id"]
			name = value["name"]
			champ = Champ.get_champ(id,name)
			champ.save()




