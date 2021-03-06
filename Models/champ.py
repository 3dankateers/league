## Champ: champID, name, winrate, winrate_sample_size 

from db_client import DbClient

class Champ:
    def __init__(self, champID, name, winrate = None, winrate_sample_size = None):
        self.champID = champID
        self.name = name
        self.winrate = winrate
        self.winrate_sample_size = winrate_sample_size

    @classmethod
    def from_tuple(cls, tup):
        c = Champ(tup[0], tup[1], tup[2], tup[3])
        return c 
    
    def save(self):
        c = DbClient.get_cursor()
        c.execute("INSERT INTO Champs VALUES (%s,%s,%s,%s);", (self.champID, self.name, self.winrate, self.winrate_sample_size))
        DbClient.get_conn().commit()
        print("Saved champ")

    def update(self):
        c = DbClient.get_cursor()
        c.execute("UPDATE Champs SET winrate = (%s), winrate_sample_size = (%s) WHERE champID = (%s);", (self.winrate, self.winrate_sample_size, self.champID, ) )
        DbClient.get_conn().commit()
        print("Updated champ")

    @staticmethod
    def get_champ_by_id(c_id):
        c = DbClient.get_cursor()
        c.execute("SELECT * FROM Champs WHERE champID = (%s);", (c_id,))
        champ = Champ.from_tuple(c.fetchone())
        return champ 
        
    
    @staticmethod
    def reset_winrates():
        c = DbClient.get_cursor()
        c.execute("UPDATE Champs SET winrate = NULL;")
        DbClient.get_conn().commit()

    ##returns array of summoners objects matching the tier and region; constructed from db
    @staticmethod
    def get_all_champs():
        champs = []
        c = DbClient.get_cursor()
        c.execute("SELECT * FROM Champs")
        rows = c.fetchall()
        for r in rows:
            c = Champ.from_tuple(r)
            champs.append(c)
        return champs 
        

    
    @staticmethod
    def get_champ_by_name(c_name):
        c = DbClient.get_cursor()
        c.execute("SELECT * FROM Champs WHERE name = (%s);", (c_name,))
        row = c.fetchone()
        return Champ.from_tuple(row)

    ##takes in an array of champ names, returns array of corresponding ids
    @staticmethod
    def names_to_ids(names):
        ids = []
        for n in names:
            ids.append(Champ.get_champ_by_name(n).champID)
        return ids


