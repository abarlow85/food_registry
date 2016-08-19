class Food2ForkAPI(object):
	key = "d40b90968cc0a0052dd0155deb54550f"
	def search(self, term):
		return "http://food2fork.com/api/search?key="+self.key+"&q="+term+"&sort=r&page=1"
	def getOne(self, id):
		return "http://food2fork.com/api/get?key="+self.key+"&rId="+id