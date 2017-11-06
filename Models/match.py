## match : id, team1, team2, champs1, champs2, first_blood, duration, win, patch, region, gameVersion, tier, date

from db_client import DbClient
import json

class Match:

    WIN = "win"	
    def __init__(self, gameID, team1, team2, champs1, champs2, first_blood, duration, win, gameType, region, patch, tier, date, is_test = False):
        self.gameID = gameID
        self.team1 = team1
        self.team2 = team2
        self.champs1 = champs1
        self.champs2 = champs2
        self.first_blood = first_blood
        self.duration = duration
        self.win = win
        self.gameType = gameType
        self.region = region
        self.patch = patch
        self.tier = tier
        self.date = date
        self.is_test = is_test ## when set to true, used for testing, when false used for training 
    

    ## push match into database
    def save(self):
        c = DbClient.get_cursor()
        ##json.dumps to encode arrays of champs1, champs2 into JSON
        json_champs1 = json.dumps(self.champs1)
        json_champs2 = json.dumps(self.champs2)
        c.execute("INSERT INTO Matches VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?);", (self.gameID, self.team1, self.team2, json_champs1, json_champs2, self.first_blood, self.duration, self.win, self.gameType, self.region, self.patch, self.tier, self.date, self.is_test))
        DbClient.get_conn().commit()

    ##update existing match
    def update(self):
        c = DbClient.get_cursor()
        c.execute("UPDATE Matches SET is_test = (?) WHERE gameID = (?);", (self.is_test, self.gameID,))
        DbClient.get_conn().commit()

        
	
    ## returns a match object from a tuple fetched from sqllite db
    @staticmethod
    def from_tuple(tup):
        ##json loads to decode json back into arrays for champs1, champs2
        m = Match(tup[0], tup[1], tup[2], json.loads(tup[3]), json.loads(tup[4]), tup[5], tup[6], tup[7], tup[8], tup[9], tup[10], tup[11], tup[12], tup[13])
	return m
   
    ## gets training set of matches(where is_test = false)
    @staticmethod
    def get_training_set():
        matches = []
        c = DbClient.get_cursor()
        c.execute("SELECT * FROM Matches WHERE is_test = (?);", (False,))
        rows = c.fetchall()
        for r in rows:
            m = Match.from_tuple(r)
            matches.append(m)
        return matches
    
    ## gets test set of matches(where is_test = true)
    @staticmethod
    def get_test_set():
        matches = []
        c = DbClient.get_cursor()
        c.execute("SELECT * FROM Matches WHERE is_test = (?);", (True,))
        rows = c.fetchall()
        for r in rows:
            m = Match.from_tuple(r)
            matches.append(m)
        return matches

    ## sets is_test = False for all matches in db
    @staticmethod
    def remove_all_tests():
        c = DbClient.get_cursor()
        c.execute("UPDATE Matches SET is_test = (?);", (False,)) 
        DbClient.get_conn().commit()
        
	
