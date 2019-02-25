from tinydb import TinyDB, Query
import json


class DB(object):
	def __init__(self, path):
		self.path = path
		self.db = TinyDB(self.path + '/db.json')

	def get_all(self, table):
		return self.db.table(table).all()

	def get(self, table, match_filter):
		match_filter = json.loads(match_filter)
		Match = Query()
		res = self.db.table(table).search(
											(Match.deckId.one_of(match_filter['decks']))
											& (Match.gameType.one_of(match_filter['modes']))
											& (Match.timestamp.test(self.between_times, match_filter['timeframe']['startTime'], match_filter['timeframe']['endTime']))
		)
		return res

	def insert_many(self, num):
		for i in range(num):
			self.db.table('matches').insert({'result': 'win'})
		return null

	def all(self):
		return self.db.all()

	def between_times(self, val, startTime, endTime):
		return startTime <= val <= endTime