<template>
  <li class="match">
    <div>
      <p class="opponentHeader">{{ 'Match vs ' + match.opponent.displayName }}</p>
      <p class="time">{{ match.timestamp | makeUTCReadable }}</p>
      <p>{{ match.gameType }}</p>
      <p>{{ match.result | capitalize }}</p>
      <p>{{ 'Deck: ' + match.deckName }}</p>
      <ul>
        <li v-for="game in match.games">
          <p>Game {{ game.gameNumber }}</p>
          <p>{{ game. result }}</p>
          <p> {{ game.reason }}</p>
        </li>
      </ul>
    </div>
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
    filters: {
      uppercase(text) {
        return text.toUpperCase()
      },
      capitalize(text) {
        return text.charAt(0).toUpperCase() + text.slice(1)
      },
      makeUTCReadable(utcString) {
        let date = new Date(parseInt(utcString)*1000)
        let formattedDate = [date.getMonth()+1, date.getDate(), date.getFullYear()].join('/')
        let hours = date.getHours()
        let amPM = ''
        if (hours === 12) {

        }

        let formattedTime = date.getHours() + ':' + date.getMinutes()
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
  .time {
    width: 20%;
  }
  .opponentHeader {
    width: 80%;
  }
  p {
    display: inline-block;
  }
</style>
