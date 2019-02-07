<template>
  <div id="app">
    <ul>
      <li v-for="match in matches">{{ match.matchId }}</li>
    </ul>
  </div>
</template>

<script>
  // import HelloWorld from './components/HelloWorld.vue'
  import ZerorpcClient from './zerorpcClient.js'

  export default {
    name: 'app',
    components: {
      // HelloWorld
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
  #app {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    margin-top: 60px;
  }
</style>