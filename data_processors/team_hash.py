## returns hash value from a team

class TeamHash:
	## returns hash key from list of summoner ids
	@staticmethod
	def calc_hash_key(summoners):
		product = 1
		for s in summoners:
			product *= long(s)
		return product

