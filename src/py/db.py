from tinydb import TinyDB, Query

class DB(object):
	def __init__(self, path):
		self.path = path
		self.db = TinyDB(self.path + '/db.json')
		# self.tables = ['matches']
		# for i in self.tables:
		# 	self.db.table(i)
	def get_all(self, table):
		return self.db.table(table).all()
	def insert_many(self, num):
		for i in range(num):
			self.db.table('matches').insert({'result': 'win'})
		return null
	def all(self):
		return self.db.all()