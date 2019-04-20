<template>
  <div id="app">
    <div class="header">
      <h1>MTGA Match History Viewer</h1>
    </div>
    <nav>
      <aside>
        <ul>
          <li :class="{ selectedView: (currentView == 'MatchHistory') }" v-on:click="currentView = 'MatchHistory'">Match History</li>
          <li :class="{ selectedView: (currentView == 'Graphs') }" v-on:click="currentView = 'Graphs'">Graphs</li>
        </ul>
      </aside>
    </nav>
    <keep-alive>
      <component class="component" v-bind:is="currentViewComponent"></component>
    </keep-alive>
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
    background-color: #090909;
    color: rgba(255,255,255,.9);
    font-weight: lighter;
    height: 100vh;
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
  }
  #app:hover {
    cursor: default;
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
    margin: 0;
    font-weight: lighter;
    font-size: 1.75em;
    text-align: left;
  }
  nav {
    width: 225px;
    font-size: 1.5em;
    background-color: #111;
    border-right: 2px solid #090909;
  }
  ul {
    list-style: none;
    padding-left: 20px;
    text-align: left;
  }
  li {
    margin-bottom: 1em;
    cursor: pointer;
  }
  .component {
    width: calc(100vw - 225px);
    height: 100%;
    background-color: #111;
  }
  .selectedView {
    color: #f37426;
  }
</style>