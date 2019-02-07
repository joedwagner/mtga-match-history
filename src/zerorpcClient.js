const zerorpc = require("zerorpc")
const app = require('electron').remote.app

/*****

Section 1: Class Definition

ZerorpcClient: Class for handling connection to and requests to the Python zerorpc server 

*****/

class ZerorpcClient {

  constructor() {
    this.client = new zerorpc.Client()
    this.client.connect('tcp://127.0.0.1:4242')
    this.initDB()
  }

  initDB() {
    this.client.invoke('init_db', app.getPath('userData'), (err, res) => {
      return null
    })
  }

  getAllMatches(cb) {
    this.client.invoke("get_all_matches", (err, res) => {
      if (err) {
        cb(err, null)
      } else {
        cb(null, res)
      }
    })
  }
}

export default ZerorpcClient