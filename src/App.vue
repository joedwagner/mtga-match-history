<template>
  <div id="app">
    <div class="header">
      <h1>MTGA Match History Viewer</h1>
    </div>
    <div class="filtersBox">
      <div>
        <label for="dateFilter">Date</label><input id="dateFilter" type="date">
      </div>
      <dropdown :options="['Play', 'Constructed', 'Ranked']"></dropdown>
      <div>
        <label for="deckFilter">Deck</label><input id="deckFilter">
      </div>
    </div>
    <div class="matchListBox">
      <h2>Matches</h2>
      <ul class="matchList">
        <match v-for="match in matches" :match=match></match>
      </ul>
    </div>
    <div class="statBox">
      <h2>Statistics</h2>
    </div>
    </div>
    
  </div>
</template>

<script>
  import Match from './components/Match.vue'
  import Dropdown from './components/Dropdown.vue'
  import ZerorpcClient from './zerorpcClient.js'

  export default {
    name: 'app',
    components: {
      Match,
      Dropdown
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
    background-color: #080808;
    color: rgba(255,255,255,.9);
    font-weight: lighter;
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    justify-content: space-around;
  }
  .filtersBox {
    width: 100%;
    margin: 20px;
    text-align: left;
    display: flex;
    flex-direction: row;
    justify-content: space-around;
  }
  .matchListBox {
    width: 40%;
    padding: 15px
  }
  .matchList {
    list-style-type: none;
    margin: 0 0;
    border: 1px solid rgba(144,238,144,1);
    margin: 20px 15px 20px 15px;
    padding: 0;
  }
  .statBox {
    width: 40%;
    padding: 15px;
  }
  .header {
    background-color: #080808;
    padding: 10px;
    color: rgba(255,255,255,.9);
    width: 100%;
  }
  body {
    margin: 0;
  }
  h1 {
    margin-top: 0;
    margin-bottom: 0;
    font-weight: lighter;
    font-size: 3em;
  }
  h2 {
    font-weight: lighter;
    margin: 0;
  }
  .match:last-child {
    border-bottom: 0px;
  }
  .recentStats {
    padding: 10px;
  }
</style>