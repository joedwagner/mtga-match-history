from tinydb import TinyDB, Query
import json
import pytz
from datetime import datetime, time, timedelta
from tzlocal import get_localzone


class DB(object):
	def __init__(self, path):
		self.path = path
		self.db = TinyDB(self.path + '/db.json')

	def get_all(self, table):
		return self.db.table(table).all()

	def get_matches(self, in_filters):
		query = Query()
    
		filters = json.loads(in_filters)

		matches = self.db.table('matches')
		gametypes = filters['modes']
		decks = filters['decks']
    
		timePeriodEnd = int(datetime.now().astimezone(get_localzone()).astimezone(pytz.utc).timestamp())
		# 'switch/case' for timeperiod
		if filters['timeframe']=='All Time':
			timePeriodStart = 0
		elif filters['timeframe']=='Today':
			timePeriodStart = int(datetime.combine(datetime.today(), time.min).astimezone(get_localzone()).astimezone(pytz.utc).timestamp())
		elif filters['timeframe']=='7 Days':
			timePeriodStart = int((datetime.combine(datetime.today(), time.min)-timedelta(days=7)).astimezone(get_localzone()).astimezone(pytz.utc).timestamp())
		elif filters['timeframe']=='This Week':
			timePeriodStart = int((datetime.combine(datetime.today(), time.min)-timedelta(days=datetime.now().weekday())).astimezone(get_localzone()).astimezone(pytz.utc).timestamp())
		elif filters['timeframe']=='30 Days':
			timePeriodStart = int((datetime.combine(datetime.today(), time.min)-timedelta(days=30)).astimezone(get_localzone()).astimezone(pytz.utc).timestamp())
		elif filters['timeframe']=='This Month':
			timePeriodStart = int(datetime(datetime.today().year,datetime.today().month,1,0,0).astimezone(get_localzone()).astimezone(pytz.utc).timestamp())
		elif filters['timeframe']=='365 Days':
			timePeriodStart = int((datetime.combine(datetime.today(), time.min)-timedelta(days=365)).astimezone(get_localzone()).astimezone(pytz.utc).timestamp())
		elif filters['timeframe']=='This Year':
			timePeriodStart = int(datetime(datetime.today().year,1,1,0,0).astimezone(get_localzone()).astimezone(pytz.utc).timestamp())
		elif filters['timeframe']=='Custom':
			timePeriodStart = 'a bunch of bullshit'
			timePeriodEnd = 'followed by even more bullshit'
		
		mDict = matches.search((query.gameType.one_of(gametypes)) &
							(query.deckId.one_of(decks)) &
							(query.timestampEnd>timePeriodStart)&
							(query.timestampEnd<timePeriodEnd))
		
		mWinCount = 0
		gWinCount = 0
		gCount = 0
		mTimeList = list()
		gTimeList= list()
		
		for i in range(0,len(mDict)):
			# win/loss ratio
			if mDict[i]['result']=='Win':
				mWinCount += 1
			
			# match times
			mTimeList.append(mDict[i]['timestampEnd']-mDict[i]['timestampStart'])
		
			# game time
			for g in range(0,len(mDict[i]['games'])):
				gTimeList.append(mDict[i]['games'][g]['timestampEnd']-mDict[i]['games'][g]['timestampStart'])
				
				if mDict[i]['games'][g]['result']=='Win':
					gWinCount += 1
			
				gCount += 1
		stats = dict()
		if not len(mDict)==0:
			stats['matchWinPct'] = (mWinCount/len(mDict))*100
			stats['gameWinPct'] = (gWinCount/gCount)*100
			
			stats['matchAvgTime'] = sum(mTimeList)/len(mTimeList)
			stats['gameAvgTime'] = sum(gTimeList)/len(gTimeList)

		output = dict([('stats',stats),('matches',mDict)])

		with open('matches.json','w') as outfile: 
			json.dump(output,outfile)
			
		return output

	def insert_many(self, num):
		for i in range(num):
			self.db.table('matches').insert({'result': 'win'})
		return null

	def all(self):
		return self.db.all()

	def between_times(self, val, startTime, endTime):
		return startTime <= val <= endTime