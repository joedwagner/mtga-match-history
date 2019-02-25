import zerorpc
from db import DB


class RPC(object):
	def init_db(self, path):
		self.conn = DB(path)
		return None

	def get_all_matches(self):
		return self.conn.get_all('matches')

	def insert_many(self, number):
		self.conn.insert_many(number)
		return None

	def get_matches(self, match_filter):
		return self.conn.get('matches', match_filter)


def main():
	# Start server using TCP on port 4242
	server = zerorpc.Server(RPC())
	server.bind('tcp://0.0.0.0:4242') 
	server.run()


if __name__ == '__main__':
	main()