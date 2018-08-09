## pair: id, champ1, champ2, type, winrate, winrate_sample_size
## looks for winrates among pairs of champions from opposite or same teams(type)
from db_client import DbClient

class Pair:
    def __init__(self, champ1, champ2, type, winrate = None, winrate_sample_size = None, pairID = None):
        ## pair ignores order of champ1/champ2 passed in
        self.pairID = Pair.calc_id(champ1, champ2, type)
        self.pair_tuple = Pair.calc_pair_tuple(champ1,champ2)
        self.champ1 = self.pair_tuple[0]
        self.champ2 = self.pair_tuple[1]
        self.type = type
        self.winrate = winrate
        self.winrate_sample_size = winrate_sample_size
    
    @classmethod
    def from_tuple(cls, tup):
        p = Pair(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5])
        return p 

    ## calculates unique id given champ1, champ2, type
    @staticmethod
    def calc_id(champ1, champ2, type):
        tup = Pair.calc_pair_tuple(champ1, champ2)
        id = int(str(tup[0])+ "0000" + str(tup[1]))
        if type == "enemy":
                id *= -1
        return id

    @staticmethod
    def calc_pair_tuple(c1,c2):
        sorted_champs = [c1, c2]
        sorted_champs.sort()
        pair_tuple = (sorted_champs[0], sorted_champs[1])
        return pair_tuple
    
    def save(self):
        c = DbClient.get_cursor()
        c.execute("INSERT INTO Pairs VALUES (%s,%s,%s,%s,%s,%s);", (self.champ1, self.champ2, self.type, self.winrate, self.winrate_sample_size, self.pairID))
        DbClient.get_conn().commit()
        print("Saved pair")
    

    ## delete all documents
    @staticmethod
    def drop_all():
        c = DbClient.get_cursor()
        c.execute("DELETE FROM Pairs;")
        DbClient.get_conn().commit()

    ## find pair and return it based on champ1, champ2, and type
    @staticmethod
    def get_pair_by_id(p_id):
        c = DbClient.get_cursor()
        c.execute("SELECT * FROM Pairs WHERE pairID = (%s);", (p_id,))
        data = c.fetchone()
        if data != None:
            return Pair.from_tuple(data)
        else:
            return None

    ##takes in an array of tuples, a tuple is info for a pair. Inserts all at once into db
    ## this is neccesary since db.commit() is expensive
    @staticmethod
    def insert_from_tuples(p_tuples):
        c = DbClient.get_cursor()
        for t in p_tuples:
            pairID = Pair.calc_id(t[0], t[1], t[2])
            c.execute("INSERT INTO Pairs VALUES (%s,%s,%s,%s,%s,%s);", (t[0], t[1], t[2], t[3], t[4], pairID))
        DbClient.get_conn().commit()
        print("Saved pairs from tuples")
        
