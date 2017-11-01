################################################################################################
## mondodb api
## db: league
##
## collections: summoners, matches, teams, champs, pairs
## Summoner: id, name, tier, division, region, date_scraped_peers, date_scraped_matches
## Match : id, team1, team2, champs1, champs2, duration, win, gametype, region, patch, tier, date
## Team : id, summoners, matches, date_created 
## Champ: id, name, winrate, winrate_sample_size
## pair: id, champ1, champ2, type, winrate, winrate_sample_size, date_created
#################################################################################################
import sqlite3



class DbClient:

    conn = None

    @staticmethod
    def get_conn():
        if DbClient.conn == None:
            DbClient.conn = sqlite3.connect('data/league.sqlite')
        return DbClient.conn
            
        

    @staticmethod
    def get_cursor():
        return DbClient.get_conn().cursor()
        


    @staticmethod
    def create_tables():
        c = DbClient.get_cursor()
        c.execute("CREATE TABLE IF NOT EXISTS Matches (gameID, team1, team2, champs1, champs2, first_blood, duration, win, gametype, region, patch, tier, date);")
        c.execute("CREATE TABLE IF NOT EXISTS Summoners (summonerID, accountID, tier, region, date_scraped_matches);")
        DbClient.get_conn().commit()
            
                
