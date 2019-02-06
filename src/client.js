const zerorpc = require("zerorpc")
const app = require('electron').remote.app

const client = new zerorpc.Client()
client.connect("tcp://127.0.0.1:4242")

client.invoke("init_db", app.getPath('userData'))
// client.invoke("insert_many", 100, (error, res) => {
//   if (error) {
//     console.log(error)
//   }
// })
client.invoke("get_all_matches", (error, res) => {
  console.log(res);
})