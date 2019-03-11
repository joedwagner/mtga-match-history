<template>
  <div id="app">
    <div class="header">
      <h1>MTGA Match History Viewer</h1>
    </div>
    <nav>
      <aside>
        <ul>
          <li v-on:click="currentView = 'MatchHistory'">Match History</li>
          <li v-on:click="currentView = 'Graphs'">Graphs</li>
        </ul>
      </aside>
    </nav>
    <component class="component" v-bind:is="currentViewComponent"></component>
  </div>
</template>

<script>

  import MatchHistoryView from './components/MatchHistoryView.vue'
  import GraphsView from './components/GraphsView.vue'

  export default {
    name: 'app',
    components: { 
      MatchHistoryView,
      GraphsView
    },
    data() {
      return {
        currentView: 'MatchHistory' 
      }
    },
    computed: {
      currentViewComponent() {
        return this.currentView + 'View'
      }
    }
  }
</script>

<style>
  #app {
    text-align: center;
    font-family: 'Montserrat', sans-serif;
    background-color: #080808;
    color: rgba(255,255,255,.9);
    font-weight: lighter;
    height: 100vh;
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
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
  nav {
    width: 20%;
  }
  .component {
    width: 80%;
  }
</style>