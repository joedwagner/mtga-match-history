<template>
  <li class="match">
      <p class="opponentHeader">{{ 'Match vs ' + opponentDisplayNameWithoutNumbers }}</p>
      <p class="dateText">{{ match.timestampEnd | UTCto12HourTime }}</p>
      <div class="deckDisplayBox box">
        <p class="boxHeader">Deck</p>
        <p>{{ match.deckName }}</p>
      </div>
      <div class="box">
        <p class="boxHeader">Mode</p>
        <p>{{ match.gameType }}</p>
      </div>
      <div class="resultBox box">
        <p v-bind:result="match.result.toLowerCase()" class="resultText boxHeader">{{ match.result | capitalize }}</p>
        <p class="gameScore">{{ gamesWon + ' - ' + gamesLost }}</p>
        <p class="tiny-text">Game Score</p>
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
      },
      opponentDisplayNameWithoutNumbers() {
        let displayName = this.match.opponent.displayName
        let indexOfPound = displayName.indexOf('#')
        return displayName.substring(0, indexOfPound)
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
    justify-content: space-between;
    color: rgba(255,255,255,.8);
    background-color: #19181A;
  }
  .match:hover {
    background-color: rgba(50, 48, 52, 1);
  }
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
  .matchBox {
    width: 30%;
  }
  .resultBox {
    width: 30%;
  }
</style>
