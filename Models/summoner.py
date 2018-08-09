## Summoner: playerid, summonerid, tier, region, date_scraped_matches

from db_client import DbClient

class Summoner:
    def __init__(self, summonerID, accountID, tier, region, queueId, date_scraped_matches = None):
        self.summonerID = summonerID
        self.accountID = accountID 
        self.tier = tier
        self.region = region
        self.date_scraped_matches = date_scraped_matches
        self.queueId = queueId


    ##saves Summoner to db
    def save(self):
        c = DbClient.get_cursor()
        c.execute("INSERT INTO Summoners VALUES (%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING;", (self.summonerID, self.accountID, self.tier, self.region, self.queueId, self.date_scraped_matches))
        DbClient.get_conn().commit()
        print("Saved summoner")

    ##returns array of summoners objects matching the tier and region; constructed from db
    @staticmethod
    def get_summoners(region, tier, queue):
        summoners = []
        c = DbClient.get_cursor()
        c.execute("SELECT * FROM Summoners WHERE tier=(%s) AND region=(%s) AND queueId = (%s)", (tier,region,queue,))
        rows = c.fetchall()
        for r in rows:
            s = Summoner.from_tuple(r)
            summoners.append(s)
        return summoners

        
	#Need this to delete dead accounts now or a more cerebral way to cleanse the infestation
    #   of trash players who got demoted from challengers later
    @staticmethod
    def delete_summoner(accID):
        print("deleted summoner",  accID)
        c = DbClient.get_cursor()
        c.execute ("DELETE FROM Summoners WHERE accountID=(%s);", (accID,))

    ## returns a Summoner object from a tuple fetched from sqllite db
    @staticmethod
    def from_tuple(tup):
        s = Summoner(tup[0], tup[1], tup[2], tup[3], tup[4])
        return s

				
