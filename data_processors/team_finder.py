############################################################################
## analyzes data from db and finds teams
## inserts relevant teams into db
## relevant team: team of 4 or 5 ppl who play more than 2 matches together
############################################################################
from match import Match
from team import Team
from team_match_occurance import TeamMatchOccurance
from team_hash import TeamHash
from collections import namedtuple

##min requirement of matches played together to be considered a relevant "team"
NUM_MATCH_REQUIREMENT = 3

##holds information about a team
## player ids is an array of the player ids (uniquely defines teaminfo)
## match_ids is an array of all the matches team played in
## sides is an array corresponding to match_ids array that holds 100 or 200 depending on what side team is on
class TeamInfo:
	def __init__(self, player_ids, match_id, side):
		self.player_ids = player_ids
		self.match_ids = [match_id]
		self.sides = [side]
	
	## adds another instance of a match this team has played in
	def add_match(self, match_id, side):
		self.match_ids.append(match_id)
		self.sides.append(side)


class TeamFinder:
	
	def __init__(self):
		## dictionary holds all team infos found, uniquely defined by key which is a tuple
		self.potential_team_infos = {}

	## find all relevant teams
	## insert all relevant teams into db
	## update matches to cointain premade information
	def run(self):
		Team.drop_all()
		self.find_all_potential_teams()
		self.insert_db_relevant_teams()
		self.update_matches_premade()
	
	##insert into db all relevant teams(have multiple matches)
	def insert_db_relevant_teams(self):
		for key, value in self.potential_team_infos.iteritems():
			## ensure each team has a sufficient number of matches
			if len(value.match_ids) >= NUM_MATCH_REQUIREMENT:
				team = Team.get_team(value.player_ids, value.match_ids, value.sides)
				team.save()

	## analyze all matches to find reoccuring teams
	## add relevant teams to db
	def find_all_potential_teams(self):
		cursor = Match.get_testable_set()
		for d in cursor:
			match = Match.from_dict(d)
			
			##this will populate team infos with teams extracted from the match
			self.populate_team_infos_from_match(match)

	## takes in a match and adds all potential teams to potential_team_infos
	def populate_team_infos_from_match(self, match):
		potential_big_team1 = match.team1
		potential_big_team2 = match.team2
		m_id = match.id
		self.populate_team_infos_from_team(potential_big_team1, m_id, 100)
		self.populate_team_infos_from_team(potential_big_team2, m_id, 200)
	
	## given a team of 5 players, generate 6 possible teams and add them to potential_team_infos
	def populate_team_infos_from_team(self, player_ids, m_id, side):
		
		##sort player_ids first to ensure no duplicates
		player_ids = sorted(player_ids)
		

		## tuple used to index dictionary	
		tup = (player_ids[0], player_ids[1], player_ids[2], player_ids[3], player_ids[4])  
		
		##if team already in potential_team_infos, update with new match info
		if tup in self.potential_team_infos:
			self.potential_team_infos[tup].add_match(m_id, side)
		else:
			big_team_info = TeamInfo(player_ids, m_id, side)
			self.potential_team_infos[tup] = big_team_info
		
		##add all possible teams of 4 to all_teams
		for i in range(5):
			player_ids_4 = player_ids[0:i] + player_ids[i+1:5] 
		

			## tuple used to index dictionary	
			tup = (player_ids_4[0], player_ids_4[1], player_ids_4[2], player_ids_4[3])  
			##if team already in potential_team_infos, update with new match info
			if tup in self.potential_team_infos:
				self.potential_team_infos[tup].add_match(m_id, side)
			else:
				new_team_info = TeamInfo(player_ids_4, m_id, side)
				self.potential_team_infos[tup] = new_team_info


	##loop through all accepted teams
	##update is_team1 or is_team2 to hold information about whether there is a premade team on side1 or side2
	def update_matches_premade(self):
		for key, ti in self.potential_team_infos.iteritems():
			## ensure each team has a sufficient number of matches
			if len(ti.match_ids) >= NUM_MATCH_REQUIREMENT:
				for i in range(len(ti.match_ids)):
					m_id = ti.match_ids[i]
					side = ti.sides[i]
					match = Match.get_match(m_id)
					##update whether there is a team on side 1 or 2 of that match
					if side == 100:
						match.is_team1 = True
					elif side == 200:
						match.is_team2 = True
					match.save()

					

