<template>
  <div id="matchHistoryView">
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
        :sorted="true"
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
    <div class="statsBox">
      <!-- <h2>Statistics</h2> -->
      <div v-if="stats">
        <p class="stat-line">Match win percentage: {{ stats.matchWinPct | toTwoDigits }}%</p>
        <p class="stat-line">Average match duration: {{ stats.matchAvgTime | secondsToMinutes }}</p>
        <p class="stat-line">Game win percentage: {{ stats.gameWinPct | toTwoDigits }}%</p>
        <p class="stat-line">Average game duration: {{ stats.gameAvgTime | secondsToMinutes }}</p>
      </div>
    </div>
    <div class="matchListBox">
      <ul class="matchList" v-if="sortedFilteredMatches" v-show="sortedFilteredMatches.length > 0" @scroll="checkLoadMore">
        <match v-for="match in currentPageMatches" :key=match.matchId :match=match></match>
      </ul>
      <p class="noMatches" v-if="sortedFilteredMatches" v-show="sortedFilteredMatches.length === 0">Sorry, no matches were found. :(<br><br>Try again using different search criteria.</p>
      <p class="matchCount" v-if="sortedFilteredMatches" v-show="sortedFilteredMatches.length > 0">Displaying {{ currentPageMatches.length }} of {{ sortedFilteredMatches.length }} matches</p>    
    </div>
  </div>
</template>

<script>
  import Match from './Match.vue'
  import Dropdown from './Dropdown.vue'
  import ZerorpcClient from '../zerorpcClient.js'
  import Datepicker from 'vuejs-datepicker'
  import MultiSelectDropdown from './MultiSelectDropdown.vue'

  export default {
    name: 'match-history-view',
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
        timeframeList: ['All Time', 'Today', '7 Days', '30 Days', '365 Days'],
        timeframeCustom: 'Custom Range',
        filters: {
          decks: null,
          modes: null,
          timeframe: null
        },
        showDatePickerBox: false,
        dateStart: null,
        dateEnd: null,
        stats: null,
        numVisiblePages: 1,
        pageSize: 20
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
      currentPageMatches() {
        let numMatches = this.numVisiblePages*this.pageSize;
        if (numMatches <= this.sortedFilteredMatches.length) {
          return this.sortedFilteredMatches.slice(0, numMatches);
        } else {
          return this.sortedFilteredMatches;
        }
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
    mounted() {
      require('electron').ipcRenderer.on('matches-updated', () => {
        this.sendFilters();
      })
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
              this.stats = Object.keys(res.stats).length ? res.stats : null
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
        },
        checkLoadMore (event) {
          if (event.target.scrollTop + event.target.offsetHeight > event.target.scrollHeight) {
            this.loadNextPage();
          }
        },
        loadNextPage() {
          this.numVisiblePages += 1;
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
    filters: {
      toTwoDigits(val) {
        if (typeof val == 'string') {
          val = parseFloat(val)
        }
        return val.toFixed(2)
      },
      secondsToMinutes(val) {
        // Round to nearest second
        val = Math.round(val)
        return String(Math.floor(val / 60)) + 'm ' + String(val % 60) + 's'
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
  #matchHistoryView {
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    justify-content: space-around;
  }
  .dropdown {
    width: 30%;
    height: 0px;
    cursor: pointer;
  }
  .match {
    margin: 0;
  }
  .listOption {
    margin: 0;
  }
  .allOption {
    margin: 0;
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
    width: 100%;
    margin: 10px;
    text-align: left;
    display: flex;
    flex-direction: row;
    justify-content: space-around;
    flex-wrap: wrap;
    color: rgba(255,255,255,.9);
  }
  .matchListBox {
    width: 100%;
    height: 80vh;
    padding-left: 5%;
  }
  .matchList {
    list-style-type: none;
    margin: 0;
    padding: 0;
    border: 1px solid rgba(144,238,144,1);
    max-height: 60vh;
    overflow-y: scroll;
    width: 80%
  }
  .statsBox {
    width: 100%;
    margin: 10px;
    margin-top: 20px;
  }
  .stat-line {
    width: 35%;
    display: inline-block;
    font-size: .8em;
    text-align: left;
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
  .left {
    text-align: left;
  }
  .matchCount {
    
  }
</style>