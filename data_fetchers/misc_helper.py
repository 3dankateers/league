##Helper functions for parser

SCRAPE_RESET_DAYS = 10

class MiscHelper:
	## return true if never scraped or scraped really long time ago (true allows new scrape)
	@staticmethod
	def check_time_diff(dt_past):	
		if dt_past == None:
			##means summoner never got scraped
			return True
		else:
			time_elapsed = datetime.datetime.utcnow() - dt_past
			if time_elapsed.days > SCRAPE_RESET_DAYS:
				return True
			else:
				##TODO make a global request staggerer
				##sleep to prevent too many request
				time.sleep(5)
				return False

	##check if game is relevant(5v5 ranked)
	@staticmethod
	def check_game_type(g):
		if (g["gameType"] == "MATCHED_GAME") and (g["subType"] == "RANKED_SOLO_5x5"):
			return True
		else:
			return False


	## dict converts string to corresponding value so comparisons can be made
	tier_converter = {
			"CHALLENGER" : 1,
			"MASTER" : 2,
			"DIAMOND" : 3,
			"PLATINUM" : 4,
			"GOLD" : 5,
			"SILVER" : 6,
			"BRONZE" : 7,
			"UNRANKED" : 8}
