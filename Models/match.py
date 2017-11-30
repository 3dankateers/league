## match : id, team1, team2, champs1, champs2, first_blood, duration, win, patch, region, gameVersion, tier, date, is_test

from db_client import DbClient
import json
import datetime

CUR_PATCH = "7.22.208.1062"
##CUR_PATCH = "7.21.206.6866"
##CUR_PATCH = "7.23.209.7302"

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

        UNIXDate = self.date/1000

        realDate = datetime.datetime.fromtimestamp(int(UNIXDate)).strftime('%Y-%m-%d')

        print realDate
        print self.gameID

        c.execute("INSERT INTO Matches (gameID, team1, team2, champs1, champs2, first_blood, duration, win, gametype, region, patch, tier, date, is_test) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING;", (self.gameID, self.team1, self.team2, json_champs1, json_champs2, self.first_blood, self.duration, self.win, self.gameType, self.region, self.patch, self.tier, realDate, self.is_test))
        DbClient.get_conn().commit()
        print "Saved match"

    ##update existing match
    def update(self):
        c = DbClient.get_cursor()
        c.execute("UPDATE Matches SET is_test = (%s) WHERE gameID = (%s);", (self.is_test, self.gameID,))
        DbClient.get_conn().commit()
        ##print "Updated match"

        
	
    ## returns a match object from a tuple fetched from sqllite db
    @staticmethod
    def from_tuple(tup):
        ##json loads to decode json back into arrays for champs1, champs2
        m = Match(tup[0], tup[1], tup[2], json.loads(tup[3]), json.loads(tup[4]), tup[5], tup[6], tup[7], tup[8], tup[9], tup[10], tup[11], tup[12], tup[13])
	return m
   
    ## gets training set of matches(where is_test = false)
    @staticmethod
    def get_training_set(cur_patch = True):
        matches = []
        c = DbClient.get_cursor()
        ##if cur_patch flag is set only return matches from cur_patch
        if cur_patch:
            p = Match.get_latest_patch()
            c.execute("SELECT * FROM Matches WHERE is_test = (%s) AND patch = (%s);", (False, CUR_PATCH,))
        else:
            c.execute("SELECT * FROM Matches WHERE is_test = (%s);", (False,))
        rows = c.fetchall()
        for r in rows:
            m = Match.from_tuple(r)
            matches.append(m)
        return matches
    

    ## gets test set of matches(where is_test = true)
    @staticmethod
    def get_test_set(cur_patch = True):
        matches = []
        c = DbClient.get_cursor()
        ##if cur_patch flag is set only return matches from cur_patch
        if cur_patch:
            p = Match.get_latest_patch()
            c.execute("SELECT * FROM Matches WHERE is_test = (%s) AND patch = (%s);", (True, CUR_PATCH,))
        else:
            c.execute("SELECT * FROM Matches WHERE is_test = (%s);", (True,))
        rows = c.fetchall()
        for r in rows:
            m = Match.from_tuple(r)
            matches.append(m)
        return matches

    ## sets is_test = False for all matches in db
    @staticmethod
    def remove_all_tests():
        c = DbClient.get_cursor()
        c.execute("UPDATE Matches SET is_test = (%s);", (False,)) 
        DbClient.get_conn().commit()
   
    ## returns most recent patch from matches in db
    @staticmethod
    def get_latest_patch():
        c = DbClient.get_cursor()
        c.execute("SELECT MAX(patch) FROM Matches")
        return c.fetchone()[0]
        DbClient.get_conn().commit()

    ##looks for matchid inside db, returns true if match exists, else false
    @staticmethod
    def exists_match(gameID):
        c = DbClient.get_cursor()
        c.execute("SELECT * FROM Matches WHERE gameID = (%s);", (gameID,))
        if len(c.fetchall()) == 0:
            return False
        else:
            return True
	
