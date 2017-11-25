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
import psycopg2



class DbClient:

    conn = None

    @staticmethod
    def get_conn():
        if DbClient.conn == None:
            ##DbClient.conn = sqlite3.connect('../league/data/league.sqlite')
            DbClient.conn = psycopg2.connect("dbname='league' user='postgres' host='localhost' password='Postgres1423'")
        return DbClient.conn
            
        

    @staticmethod
    def get_cursor():
        return DbClient.get_conn().cursor()
        

    @staticmethod
    def create_tables():
        c = DbClient.get_cursor()
        c.execute("CREATE TABLE IF NOT EXISTS Matches (gameID BIGINT PRIMARY KEY, team1 TEXT, team2 TEXT, champs1 TEXT, champs2 TEXT, first_blood INTEGER, duration INTEGER, win INTEGER, gametype TEXT, region TEXT, patch TEXT, tier TEXT, date DATE, is_test BOOLEAN);")
        c.execute("CREATE TABLE IF NOT EXISTS Summoners (summonerID INTEGER, accountID INTEGER PRIMARY KEY, tier TEXT, region TEXT, date_scraped_matches DATE);")
        c.execute("CREATE TABLE IF NOT EXISTS Champs (champID INTEGER PRIMARY KEY, name TEXT, winrate REAL, winrate_sample_size INTEGER);")
        c.execute("CREATE TABLE IF NOT EXISTS Pairs (champ1 INTEGER, champ2 INTEGER, type TEXT, winrate REAL, winrate_sample_size INTEGER, pairID INTEGER PRIMARY KEY);")
        DbClient.get_conn().commit()
            
                
