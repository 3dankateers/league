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
        c.execute("INSERT INTO Champs VALUES (?,?,?,?);", (self.champID, self.name, self.winrate, self.winrate_sample_size))
        DbClient.get_conn().commit()

    
