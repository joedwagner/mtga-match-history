import zerorpc
from db import DB
from heimdall import Watcher


class RPC(object):
	def init_db(self, path):
		self.conn = DB(path)
		return None

	def get_all_matches(self):
		return self.conn.get_all('matches')


	def get_matches(self, match_filter):
		res = self.conn.get_matches(match_filter)
		return res


def main():
	# Start server using TCP on port 4242
	server = zerorpc.Server(RPC())
	server.bind('tcp://0.0.0.0:4242') 
	server.run()


if __name__ == '__main__':
	main()