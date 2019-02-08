<template>
  <div id="app">
    <h1>Magic: The Gathering Arena</h1>
    <h2>Match History Viewer</h2>
    <ul>
      <match v-for="match in matches" :match=match></match>
    </ul>
  </div>
</template>

<script>
  import Match from './components/Match.vue'
  import ZerorpcClient from './zerorpcClient.js'

  export default {
    name: 'app',
    components: {
      Match
    },
    data () {
      return {
        matches: null
      }
    },
    created () {
      const zClient = new ZerorpcClient()
      zClient.getAllMatches((err, res) => {
        if (!err) {
          this.matches = res
        }
      })
    }
  }
</script>

<style>
  @import url('https://fonts.googleapis.com/css?family=Montserrat');
  #app {
    text-align: center;
    font-family: 'Montserrat', sans-serif;
  }
  ul {
    list-style-type: none;
    width: 60%;
    margin: 0 auto;
  }
</style>