<template>
  <li class="match">
      <p class="opponentHeader">
        {{ 'Match vs ' + opponentDisplayNameWithoutNumbers }}
        <span class="rank" v-bind:style="{color: rankColor, 'border-color': rankColor}">{{ opponentRank }}</span>
      </p>
      <p class="dateText">{{ match.timestampEnd | UTCto12HourTime }}</p>
      <div class="resultBox box">
        <p v-bind:result="match.result.toLowerCase()" class="resultText boxHeader">{{ match.result | capitalize }}</p>
        <p class="gameScore">{{ gamesWon + ' - ' + gamesLost }}</p>
        <p class="tiny-text" v-on:click="showGameList">Game Score</p>
      </div>
      <div class="deckDisplayBox box">
        <p class="boxHeader">Deck</p>
        <p>{{ match.deckName }}</p>
      </div>
      <div class="box">
        <p class="boxHeader">Mode</p>
        <p>{{ match.gameType }}</p>
      </div>
      <transition name="slide-drawer">
        <table v-show ="showGames">
          <thead>
            <tr>
              <th>Game</th>
              <th>Result</th>
              <th>Duration</th>
              <th>Turns</th>
              <th>Reason</th>
            </tr>
          </thead>
          <tr v-for="game in match.games" v-bind:key="game.gameNumber">
            <td>{{ game.gameNumber }}</td>
            <td v-bind:result="game.result.toLowerCase()">{{ game.result }}</td>
            <td>{{ game.timestampEnd - game.timestampStart | secondsToMinutes }}</td>
            <td></td>
            <td>{{ game.reason }}</td>
          </tr>
        </table>
      </transition>
  </li>
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
    border-bottom: 1px solid rgba(144,238,144,.5);
    padding: 5px 10px 5px 10px;
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    justify-content: space-around;
    color: rgba(255,255,255,.8);
    background-color: #1a1a1a;
    transition: background-color .1s ease-in;
    cursor: default;
  }
  /* .match:hover {
    background-color: #2b2b2b;
  } */
  .box {
    width: 30%;
    text-align: center;
  }
  .boxHeader {
    font-size: 1.25em;
  }
  .dateText {
    width: 30%;
    text-align: right;
    float: right;
  }
  .tiny-text {
    font-size: .8em;
    opacity: .9;
  }
  .opponentHeader {
    width: 70%;
  }
  .deckDisplayBox {
    font-size: 1em;
  }
  .resultBox {
    text-align: center;
  }
  .resultText {
    font-size: 1.25em;
  }
  [result=win] {
    color: #479761  ;
  }
  [result=loss] {
    color: red;
  }
  .rank {
    font-size: .6em;
    border: .5px solid;
    border-radius: 10px;
    padding: 4px;
    vertical-align: middle;
    opacity: .7;
    margin-left: 3px;
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
