import zerorpc

class RPC(object):
	def set_db_path(self, path):
		return(path)

def main():
	# Start server using TCP on port 4242
	server = zerorpc.Server(RPC()) 
	server.bind('tcp://0.0.0.0:4242') 
	server.run()

if __name__ == '__main__':
	main()