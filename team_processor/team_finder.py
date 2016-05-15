############################################################################
## analyzes data from db and finds teams
## inserts relevant teams into db
## relevant team: team of 4 or 5 ppl who play more than 2 matches together
############################################################################
from match import Match
from db_client import DbClient
##min requirement of matches played together to be considered a relevant "team"
MATCH_REQUIREMENT = 3

class TeamFinder:
	
	def __init__(self):
		self.teams_found = {}

	## analyze all matches to find team patters
	def find_all_teams(self):
		with DbClient() as db_client():
			cursor = db_client.get_all_matches()
			for d in cursor:
				match = Match.from_dict(d)
				m_id = match.id

	@staticmethod
	## return list of lists of Summoners representing potential teams extracted from the summoners in a match
	def potential_teams_from_match(match):
		all_teams = []
		
		big_team1 = match.team1
		big_team2 = match.team2

		all_teams = potential_teams_from_team(big_team1) + potential_teams_from_team(big_team2)
		return all_teams

	## return list of lists of Summoners representing potential teams extracted from a large 5 person team
	## returns 6 unique teams 5 of 4 members and one of 5 members
	def potential_teams_from_team(team):
		all_teams = []

		## add the one 5 man team to all_teams
		big_team = team
		all_teams.append(team)

		##add all possible teams of 4 to all_teams
		for i in range(5):
			t = team[0:i] + team[i+1:5] 
			all_team.append(t)

		return all_teams


