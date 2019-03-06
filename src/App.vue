<template>
  <div id="app">
    <div class="header">
      <h1>MTGA Match History Viewer</h1>
    </div>
    <div class="filtersBox">
      <dropdown 
        class="dropdown"
        v-if="matches"
        :options=timeframeList
        :label=timeframeLabel
        :custom=timeframeCustom
        @update-filter="updateFilters" 
        @custom-selected="showDatePickerBox = true"
        @custom-deselected="showDatePickerBox = false">
      </dropdown>
      <multi-select-dropdown
        class="dropdown"
        v-if="matches"
        :options=modeList
        :label=modeLabel
        @update-filters="updateFilters">
      </multi-select-dropdown>
      <multi-select-dropdown
        class="dropdown"
        v-if="matches"
        :options=deckList
        :label=deckLabel
        @update-filters="updateFilters">
      </multi-select-dropdown>
      <div 
        class="date-picker-box"
        v-show="showDatePickerBox">
        <datepicker placeholder="Start date" v-model="dateStart" :disabledDates="disabledStartDates" v-on:input="updateTimeframeFilter"></datepicker>
        <span>to</span>
        <datepicker placeholder="End date" v-model="dateEnd" :disabledDates="disabledEndDates" v-on:input="updateTimeframeFilter"></datepicker>
      </div>
    </div>
    <div class="matchListBox">
      <h2>Matches</h2>
      <ul class="matchList" v-if="matches">
        <match v-for="match in sortedFilteredMatches" :key=match.matchId :match=match></match>
      </ul>
      <p class="noMatches" v-if="(sortedFilteredMatches) && (sortedFilteredMatches.length === 0)">Sorry, no matches were found. :(<br>Try again using different search criteria.</p>
    </div>
    <div class="statBox">
      <h2>Statistics</h2>
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
        deckLabel: 'decks',
        modeLabel: 'modes',
        timeframeLabel: 'timeframe',
        timeframeList: ['All Time', 'Today', 'Yesterday', '7 Days', '30 Days', '365 Days'],
        timeframeCustom: 'Custom Range',
        filters: {
          decks: null,
          modes: null,
          timeframe: null
        },
        showDatePickerBox: false,
        dateStart: null,
        dateEnd: null
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
        if (!this.filteredMatches) {
          return this.matches
        } else {
          return this.filteredMatches.slice(0).sort((a,b) => {
            return b.timestampEnd - a.timestampEnd
        })
        }
      },
      disabledStartDates () {
        return {
          from: this.dateEnd ? this.dateEnd : new Date()
        }
      },
      disabledEndDates () {
        return {
          to: this.dateStart ? this.dateStart : new Date(1970, 0, 1),
          from: new Date()
        }
      }
    },
    methods: {
      updateFilters(filter) {
          switch (filter.type) {
            case 'modes':
              if (filter.filters.length === 0) {
                this.filters[filter.type] = this.modeList
              } else {
                this.filters[filter.type] = filter.filters 
              }
              break;
            case 'decks':
              if (filter.filters.length === 0) {
                this.filters[filter.type] = Object.keys(this.deckList)
              } else {
                let deckIds = []
                filter.filters.forEach((deck) => {
                  deckIds.push(deck.id)
                })
                this.filters[filter.type] = deckIds 
              }
              break;
            case 'timeframe':
              this.filters[filter.type] = filter.filter
          }
        },
        sendFilters() {
          const zClient = new ZerorpcClient();
          zClient.getMatches(this.filters, (err, res) => {
            if (!err) {
              this.filteredMatches = res.matches
            }
          })
        },
        updateTimeframeFilter () {
          if (this.dateStart && this.dateEnd) {
            this.filters.timeframe = {
              start: this.dateEnd.toLocaleDateString(),
              end: this.dateEnd.toLocaleDateString()
            }
          }
        }
    },
    watch: {
        'filters.timeframe': function() {
          this.sendFilters()
        },
        'filters.modes': function() {
          this.sendFilters()
        },
        'filters.decks': function() {
          this.sendFilters()
        }
    },
    created () {
      const zClient = new ZerorpcClient()
      zClient.getAllMatches((err, res) => {
          if (!err) {
          this.matches = res
          this.filteredMatches = res
          this.filters.decks = Object.keys(this.deckList)
          this.filters.modes = this.modeList
          this.filters.timeframe = 'All Time'
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
  /* Datepicker Styles */
  .date-picker-box {
    width: 100%;
    padding-left: 1em;
    padding-top:.5em; 
    font-size: .9em;
  }
  .vdp-datepicker {
    padding: .5em;
    display: inline-block;
  }
  .vdp-datepicker input {
    border: none;
    background-color: #19181A;
    padding: .5em;
    cursor: pointer;
    width: 100px;
    font-family: inherit;
    color: rgba(255,255,255,.8);
    text-align: center;
    border-radius: 5px;
  }
  .vdp-datepicker input:hover {
    color: #aaa;
  }
  .vdp-datepicker__calendar {
    background-color: #080808;   
    color: rgba(255,255,255,.9);
  }
  .vdp-datepicker__calendar header .next:after {
    border-left-color: rgba(255,255,255,.9);
  }
  .vdp-datepicker__calendar header .next.disabled:after {
    border: none;
  }
  .vdp-datepicker__calendar header .prev:after {
    border-right-color: rgba(255,255,255,.9);
  }
  .vdp-datepicker__calendar header .prev.disabled:after {
    border: none;
  }
  .filtersBox {
    width: 80%;
    margin: 40px;
    text-align: left;
    display: flex;
    flex-direction: row;
    justify-content: space-around;
    flex-wrap: wrap;
    color: rgba(255,255,255,.9);
  }
  .matchListBox {
    width: 60%;
    padding-left: 10%;
  }
  .matchList {
    list-style-type: none;
    margin: 0 0;
    border: 1px solid rgba(144,238,144,1);
    margin: 20px 15px 20px 15px;
    padding: 0;
    height: 60%;
    max-height: 650px;
    overflow-y: scroll;
  }
  .statBox {
    width: 20%;
    padding-right: 10%;
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