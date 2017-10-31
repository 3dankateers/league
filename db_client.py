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

    @staticmethod
    def get_conn():
        return sqlite3.connect('data/league.sqlite')
        

    @staticmethod
    def get_cursor():
        return DbClient.get_conn().cursor()
        


    @staticmethod
    def create_tables():
        c = DbClient.get_cursor()
        c.execute("CREATE TABLE IF NOT EXISTS Matches (gameID, season, champ1, champ2, champ3, champ4, champ5, champ6, champ7, champ8, champ9, champ10, winner, gameVersion);")
        c.execute("CREATE TABLE IF NOT EXISTS Summoners (summonerID, accountID, tier, region, date_scraped_matches);")
        DbClient.get_conn().commit()
            
                
