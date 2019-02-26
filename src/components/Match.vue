<template>
  <li class="match">
      <p class="opponentHeader">{{ 'Match vs ' + match.opponent.displayName + ' - ' + match.gameType }}</p>
      <p class="dateText">{{ match.timestamp | UTCto12HourTime }}</p>
      <div class="resultBox">
        <p v-bind:result="match.result.toLowerCase()" class="resultText">{{ match.result | capitalize }}</p>
        <p>{{ gamesWon + ' - ' + gamesLost }}</p>
      </div>
      <div class="deckDisplayBox">
        <p> {{ match.deckName }}</p>
      </div>
      <ul v-show ="showGames"> 
        <li v-for="game in match.games" v-bind:key="game.gameNumber">
          <p>Game {{ game.gameNumber }}</p>
          <p>{{ game.result }}</p>
          <p>{{ game.reason }}</p>
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
    border-bottom: 1px solid rgba(144,238,144,.5);
    padding: 5px 10px 5px 10px;
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    color: rgba(255,255,255,.8);
    background-color: #19181A;
  }
  .match:hover {
    background-color: rgba(50, 48, 52, 1);
  }
  .dateText {
    width: 30%;
    text-align: right;
    float: right;
  }
  .opponentHeader {
    width: 70%;
  }
  .deckDisplayBox {
    text-align: center;
    width: 30%;
    font-size: 1em;
  }
  .resultBox {
    text-align: center;
  }
  .resultText {
    font-size: 1.5em;
    margin-right: auto;
  }
  [result=win] {
    color: #479761  ;
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
