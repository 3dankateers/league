########################################################################
## parses data from league_client
## inserts new data into db
########################################################################

import datetime
import time
from summoner import Summoner
from match import Match
from db_client import DbClient
from league_client import LeagueClient
from processor_helper import ProcessorHelper

TEAM1 = 100
TEAM2 = 200
PATCH = "6.9"

class MatchProcessor:
	##given recent match data, add all new matches to db
	@staticmethod
	def populate_match_db(lc, s, data):
		games = data["games"]
		for g in games: 
			##only allow 5v5 ranked
			if ProcessorHelper.check_game_type(g):
				league_id =	g["gameId"]
					
				match = Match.get_match(league_id)
				##only proceed if match doesn't already exist
				if match == None:
					team1 = []
					team2 = []
					champs1 = []
					champs2 = []
					
					s_id = s.league_id
					s_team = g["stats"]["team"]
					s_champ = g["championId"]
					MatchProcessor.classify(team1, team2, champs1, champs2, s_id, s_champ, s_team)

					## classify current summoner in this match
					for p in g["fellowPlayers"]:
						peer_id = p["summonerId"]
						peer_team = p["teamId"]
						peer_champ = p["championId"]
						MatchProcessor.classify(team1, team2, champs1, champs2, peer_id, peer_champ, peer_team)
					
					duration = g["stats"]["timePlayed"]

					s_win = g["stats"]["win"]
					if s_team == TEAM1 and s_win:
						win = TEAM1
					elif s_team == TEAM1 and not s_win:
						win = TEAM2
					elif s_team == TEAM2 and s_win:
						win = TEAM2
					else:
						win = TEAM1

					gametype = g["subType"]
					region = lc.region
					patch = PATCH
					tier = s.tier
					date = g["createDate"]
					match = Match(league_id, team1, team2, champs1, champs2, duration, win, gametype, region, patch, tier, date)
					match.save()				


	##helper to parse match stats
	##puts player in team1 or 2 and champ1 or 2
	@staticmethod
	def classify(team1, team2, champs1, champs2, s_id, s_champ, s_team):
		if s_team == TEAM1:
			team1.append(s_id)
			champs1.append(s_champ)
		else:
			team2.append(s_id)
			champs2.append(s_champ)
	
	##crawl recent matches of summoner
	##add matches to db
	@staticmethod
	def grab_matches(lc, s):
		print "Grabbing matches of summoner: " + s.name.encode(encoding='UTF-8',errors='replace')

		## update date_scraped_peers
		s.date_scraped_matches = datetime.datetime.utcnow()
		s.save()
		
		recent_matches_data = lc.get_recent_matches_data(s.league_id)
		
		MatchProcessor.populate_match_db(lc, s, recent_matches_data)	
	
	## grab recent relevant matches by summoner
	@staticmethod
	def grab_matches_challenger(lc):
		print "Adding all matches of challengers to db"
		with DbClient() as db_client:
			cursor = db_client.get_summoners_on_tier("CHALLENGER")
			for d in cursor:
				s = Summoner.from_dict(d)
				MatchProcessor.grab_matches(lc, s)
