## Summoner: playerid, summonerid, tier, region, date_scraped_matches

from db_client import DbClient

class Summoner:
    def __init__(self, summonerID, accountID, tier, region, date_scraped_matches = None):
        self.summonerID = summonerID
        self.accountID = accountID 
        self.tier = tier
        self.region = region
        self.date_scraped_matches = date_scraped_matches


    ##saves Summoner to db
    def save(self):
        c = DbClient.get_cursor()
        c.execute("INSERT OR IGNORE INTO Summoners VALUES (?,?,?,?,?);", (self.summonerID, self.accountID, self.tier, self.region, self.date_scraped_matches))
        DbClient.get_conn().commit()
        print "Saved summoner"

    ##returns array of summoners objects matching the tier and region; constructed from db
    @staticmethod
    def get_summoners(region, tier):
        summoners = []
        c = DbClient.get_cursor()
        c.execute("SELECT * FROM Summoners WHERE tier=? AND region=?", (tier,region,))
        rows = c.fetchall()
        for r in rows:
            s = Summoner.from_tuple(r)
            summoners.append(s)
        return summoners

        
	
    ## returns a Summoner object from a tuple fetched from sqllite db
    @staticmethod
    def from_tuple(tup):
        s = Summoner(tup[0], tup[1], tup[2], tup[3], tup[4])
        return s

				
