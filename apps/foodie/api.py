class Food2ForkAPI(object):
	key = ""
	def search(self, term):
		return "http://food2fork.com/api/search?key="+self.key+"&q="+term+"&sort=r&page=1"
	def getOne(self, id):
		return "http://food2fork.com/api/get?key="+self.key+"&rId="+id