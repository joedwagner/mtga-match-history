<template>
  <li class="match">
      <p class="opponentHeader">{{ 'Match vs ' + match.opponent.displayName + ' - ' + match.gameType }}</p>
      <p class="dateText">{{ match.timestamp | UTCto12HourTime }}</p>
      <div class="matchBox">
        <p>Match score: {{ gamesWon + '-' + gamesLost }}</p>
      </div>
      <div class="resultBox">
        <p v-bind:result="match.result.toLowerCase()" class="resultText">{{ match.result | capitalize }}</p>
      </div>
      <div class="deckDisplayBox">
        <p>Deck</p>
        <p> {{ match.deckName }}</p>
      </div>
      <ul v-show ="showGames"> 
        <li v-for="game in match.games">
          <p>Game {{ game.gameNumber }}</p>
          <p>{{ game.result }}</p>
          <p> {{ game.reason }}</p>
        </li>
      </ul>
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
        showGames: false
      }
    },
    computed: {
      gamesWon() {
        return this.match.games.filter(g => g.result.toLowerCase() === 'win').length
      },
      gamesLost() {
        return this.match.games.filter(g => g.result.toLowerCase() === 'loss').length
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
      }
    }
  }
</script>

<style scoped>
  .match {
    text-align: left;
    border: 1px solid black;
    padding: 5px 10px 5px 10px;
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
  }
  .dateText {
    width: 30%;
    text-align: right;
    float: right;
  }
  .opponentHeader {
    width: 70%;
    font-weight: bold;
  }
  .deckDisplayBox {
    border: .5px solid black;
    text-align: center;
    width: 30%;
    font-size: 1em;
  }
  .resultText {
    font-size: 1.5em;
    margin-right: auto;
  }
  [result=win] {
    color: blue;
  }
  [result=loss] {
    color: red;
  }
  .matchBox {
    width: 30%;
  }
  .resultBox {
    width: 30%;
  }
</style>
