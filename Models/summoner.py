## Summoner: playerid, summonerid, tier, region, date_scraped_matches

from db_client import DbClient

class Summoner:
    def __init__(self, summonerID, accountID, tier, region, date_scraped_matches = None):
        self.summonerID = summonerID
        self.accountID = accountID 
        self.tier = tier
        self.region = region
        self.date_scraped_matches = date_scraped_matches


    def save(self):
        c = DbClient.get_cursor()
        c.execute("INSERT INTO Summoners VALUES (?,?,?,?,?);", (self.summonerID, self.accountID, self.tier, self.region, self.date_scraped_matches))
        DbClient.get_conn().commit()

				
