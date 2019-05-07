<template>
  <div class="match" v-bind:result="match.result.toLowerCase()">
    <span class="result-text" v-bind:result="match.result.toLowerCase()">{{ match.result | capitalize }}</span>
    <span class="type-text small">{{ match.gameType }}</span>
    <span class="deck-text small">{{ match.deckName }}</span>
    <span class="opponent-text small">vs. {{ opponentDisplayNameWithoutNumbers }}</span>
    <span class="rank-text" v-bind:style="{color: rankColor, 'border-color': rankColor}">{{ opponentRank }}</span>
    <span class="date-text wrap small">{{ match.timestampEnd | UTCto12HourTime }}</span>
  </div>
</template>

<script>
  export default {
    name: 'match',
    props: {
      match: {
        type: Object,
        required: true  
      }
    },
    data () {
      return {
        showGames: false,
        rankColors: {
          'bronze': '#cd7f32',
          'silver': '#c0c0c0',
          'gold': '#ffd700',
        }
      }
    },
    computed: {
      gamesWon() {
        return this.match.games.filter(g => g.result.toLowerCase() === 'win').length
      },
      gamesLost() {
        return this.match.games.filter(g => g.result.toLowerCase() === 'loss').length
      },
      opponentDisplayNameWithoutNumbers() {
        let displayName = this.match.opponent.displayName
        let indexOfPound = displayName.indexOf('#')
        return displayName.substring(0, indexOfPound)
      },
      opponentRank() {
        return this.match.opponent.rank.tier + ' ' + this.match.opponent.rank.division
      },
      rankColor() {
        return this.rankColors[this.match.opponent.rank.tier.toLowerCase()]
      }
    },
    methods: {
      showGameList() {
        this.showGames = !this.showGames
      }
    },
    filters: {
      uppercase(text) {
        return text.toUpperCase()
      },
      capitalize(text) {
        return text.charAt(0).toUpperCase() + text.slice(1)
      },
      UTCto12HourTime(utcString) {
        let date = new Date(parseInt(utcString)*1000)
        let formattedDate = [date.getMonth()+1, date.getDate(), date.getFullYear()].join('/')
        let hours = date.getHours()
        let mins = (date.getMinutes() < 10 ? '0' : '') + date.getMinutes(); 
        let amPM = ''
        if (hours >= 12) {
          amPM = 'PM'
          if (hours > 12) {
            hours -= 12
          }
        } else {
          amPM = 'AM'
          if (hours === 0) {
            hours = 12
          }
        }

        let formattedTime = hours + ':' + mins + ' ' + amPM
        return formattedDate + ' ' + formattedTime
      },
      secondsToMinutes(val) {
        // Round to nearest second
        val = Math.round(val)
        return String(Math.floor(val / 60)) + 'm ' + String(val % 60) + 's'
      }
    }
  }
</script>

<style scoped>
  .match {
    text-align: left;
    /* border-bottom: 1px solid rgba(144,238,144,.5); */
    padding: 5px 10px 5px 10px;
    color: rgba(255,255,255,.8);
    background-color: #1a1a1a;
    margin-bottom: 3px;
    display: flex;
    flex-direction: row;
    /* justify-content: space-around; */
    border-radius: 2px;
    height: 50px;
  }

  .result-text {
    width: 7%;
    font-size: 1.1em !important;
    text-align: center;
    margin-right: 3%;
    /* background: #f37426;
    height: 30px; */
  }

  .type-text {
    width: 15%;
  }

  .deck-text {
    width: 25%;
    font-size: 1em !important;
  }

  .opponent-text {
    width: 20%;
    text-decoration: underline;
    font-size: 1em !important;
  }

  .rank-text {
    width: 10%;
    font-size: .8em;
    border: .5px solid;
    border-radius: 10px;
    padding: 4px;
    vertical-align: middle;
    opacity: .7;
    margin-left: 3px;
    text-align: center;
  }

  .date-text {
    padding-left: 5% !important;
    width: 20%;
    text-align: left;
  }

  .wrap {
    white-space: normal;
  }

  .match > span {
    padding-left: 10px;
    padding-right: 10px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    padding-top: 10px;
    font-size: .9em;
  }

  .space-right {
    margin-right: 5%;
  }

  .no-margin {
    margin: 0;
  }
  .box {
    width: 30%;
    text-align: center;
  }
  .boxHeader {
    font-size: 1.25em;
  }

  .small {
    font-size: .9em;
  }

  .tiny-text {
    font-size: .8em;
    opacity: .9;
    margin-right: 5%;
  } 

  .match[result=win] {
    /* background: #f37426; */
  }

  .match[result=loss] {
    /* background: #5d26f3; */
  }

  .result-text[result=win] {
    color: green;
  }
  .result-text[result=loss] {
    color: red;
  }

  table {
    font-size: .7em;
    padding-left: 20%;
    width: 82%;
    font-weight: lighter;
    text-align: center;
    border-collapse: collapse;
  }
  th {
    font-size: 1.2em;
    font-weight: normal;
    border: 1px solid black;
    background-color: #222;
  }
  td, th {
    padding: 5px;
  }
  td {
    border-left: 1px solid black;
    border-right: 1px solid black;
  }
  tr:last-child td {
    border-bottom: 1px solid black;
  }
</style>
