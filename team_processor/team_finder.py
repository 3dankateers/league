############################################################################
## analyzes data from db and finds teams
## inserts relevant teams into db
## relevant team: team of 4 or 5 ppl who play more than 2 matches together
############################################################################
from match import Match
from db_client import DbClient
from team import Team
from team_match_occurance import TeamMatchOccurance
from team_hash import TeamHash

##min requirement of matches played together to be considered a relevant "team"
NUM_MATCH_REQUIREMENT = 3

class TeamFinder:
	
	def __init__(self):
		##dict will store all potential teams found
		##will eventually be processed such that any relevant teams it cointains are inserted into db
		self.teams_found = {}
	
	## find all relevant teams
	## insert all relevant teams into db
	def run(self):
		self.find_all_potential_teams()
		self.insert_db_relevant_teams()
	
	##insert into db all relevant teams(have multiple matches)
	def insert_db_relevant_teams(self):
		for key, value in self.teams_found.iteritems():
			if len(value) >= NUM_MATCH_REQUIREMENT:

				## gets all unique teams at that hash key(unique teams can be greater than one if unwanted collisions happened)
				unique_teams = []
				for occ in value:
					if occ.summoners not in unique_teams:
						unique_teams.append(occ.summoners)

				for t in unique_teams:
					match_list = []
					for occ in value:
						if occ.summoners == t:
							match_list += occ.match_id

					##we have relevant team
					if len(match_list) >= NUM_MATCH_REQUIREMENT:
						relevant_team = Team.get_team(t)
						relevant_team.add_matches(match_list)
						relevant_team.save()


	## analyze all matches to find reoccuring teams
	## add relevant teams to db
	def find_all_potential_teams(self):
		with DbClient() as db_client():
			cursor = db_client.get_all_matches()
			for d in cursor:
				match = Match.from_dict(d)
				m_id = match.id
				potential_teams = potential_teams_from_match(match)
				for p_team in potential_teams:
					self.add_to_teams_found(p_team, m_id)
	
	## creates team_match_occurance and adds it to teams_found dict
	def add_to_teams_found(self, p_team, m_id):
		occ = TeamMatchOccurance(p_team, m_id)
		hash_key = TeamHash.calc_hash_key(p_team)
		
		##if hash_key doesn't exit already
		if self.teams_found[hash_key] == None  
			self.teams_found[hash_key] = [occ]
		##if already exists, add new entry
		else:
			self.teams_found[hash_key].append(occ)
			
		


	## return list of lists of Summoners representing potential teams extracted from the summoners in a match
	@staticmethod
	def potential_teams_from_match(match):
		all_teams = []
		
		big_team1 = match.team1
		big_team2 = match.team2

		all_teams = potential_teams_from_team(big_team1) + potential_teams_from_team(big_team2)
		return all_teams
	
	## return list of lists of Summoners representing potential teams extracted from a large 5 person team
	## returns 6 unique teams 5 of 4 members and one of 5 members
	@staticmethod	
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


