<template>
  <div id="app">
    <div class="header">
      <h1>MTGA Match History Viewer</h1>
    </div>
    <div class="filtersBox">
      <dropdown v-if="matches" :options=timeframeList :label=timeframeLabel class="dropdown"></dropdown>
      <multi-select-dropdown v-if="matches" :options=modeList :label=modeLabel class="dropdown"></multi-select-dropdown>
      <multi-select-dropdown v-if="matches" :options=deckList :label=deckLabel class="dropdown"></multi-select-dropdown>
    </div>
    <div class="matchListBox">
      <h2>Matches</h2>
      <ul class="matchList" v-if="matches">
        <match v-for="match in sortedFilteredMatches" :match=match></match>
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
  import Datepicker from 'vuejs-datepicker'
  import MultiSelectDropdown from './components/MultiSelectDropdown.vue'

  export default {
    name: 'app',
    components: {
      Match,
      Dropdown,
      Datepicker,
      MultiSelectDropdown
    },
    data () {
      return {
        matches: null,
        filteredMatches: null,
        deckLabel: 'Decks',
        modeLabel: 'Modes',
        timeframeLabel: 'Timeframe',
        timeframeList: ['Today', 'This week', 'This month', 'This year', 'Custom range...']
      }
    },
    computed: {
      deckList () {
        let deckList = {}
        this.matches.forEach((match) => {
          if (!deckList.hasOwnProperty(match.deckId)) {
            deckList[match.deckId] = {id: match.deckId, name: match.deckName}
          }
        })
        return deckList
      },
      modeList () {
        let modeList = []
        this.matches.forEach((match) => {
          if (!modeList.includes(match.gameType)) {
            modeList.push(match.gameType)
          }
        })
        return modeList
      },
      sortedFilteredMatches () {
        return this.filteredMatches.sort((a,b) => {
          return b.timestamp - a.timestamp
        })
      }
    },
    methods: {
      filterMatches(filter) {
        console.log(filter)
      }
    },
    created () {
      const zClient = new ZerorpcClient()
      zClient.getAllMatches((err, res) => {
        if (!err) {
          this.matches = res
          this.filteredMatches = res
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
  .dropdown {
    width: 30%;
  }
  .filtersBox {
    width: 80%;
    margin: 40px;
    text-align: left;
    display: flex;
    flex-direction: row;
    justify-content: space-around;
    color: rgba(255,255,255,.9);
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
    margin-top: 20px;
    margin-bottom: 20px;
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
  .date-picker {
    color: black;
  }
</style>