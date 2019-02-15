<template>
  <div>
    <div class="label">{{ label + ':'}}</div>
    <div class="optionBox">
      <transition name="fade">
        <div class="selectedOption" v-on:click="toggleActive" v-model="selectedOption" v-bind:active="active">{{ selectedOption }}<span class="down"></span></div>
      </transition>
      <transition-group name="fade">
        <div class="option" v-if="active" v-bind:key="option" v-for="option in restOfOptions" v-on:click="selectOption">{{ option }}</div>
      </transition-group>
    </div>
  </div>
</template>

<script>
  export default {
    name: 'dropdown',
    props: {
      options: {
        type: Array,
        required: true
      },
      label: {
        type: String,
        required: false
      }
    },
    data() {
      return {
        selectedOption: this.options[0],
        active: false
      }
    },
    computed: {
      restOfOptions() {
        return this.options.filter(option => option != this.selectedOption)
      }
    },
    methods: {
      selectOption(event) {
        this.selectedOption = event.target.innerText;
        this.active = false
      },
      passFilter() {
        let filter = {}
        if (this.selectedOption === 'All') {
          filter = null
        } else {
          filter.filterType = this.label.toLowerCase(),
          filter.filterValue = this.selectedOption
        }
        this.$emit('filter-changed', filter)
      },
      toggleActive() {
        this.active = !this.active
      }
    }
  }
</script>

<style scoped>
/*  .down {
    border: solid white;
    border-width: 0 2px 2px 0;
    display: inline-block;
    padding: 5px;
    transform: rotate(45deg);
    margin-left: 5px;
  }*/
  .dropdown {
    display: flex;
    flex-direction: row;
  }
  .label {
    margin-right: 5px;
  }
  .optionBox {
    display:flex;
    flex-direction: column;
  }
  .selectedOption:hover {
    cursor: pointer;
  }
  .selectedOption {
    text-decoration: underline;
    text-align: center;
  }
  .option {
    background-color: #19181A;
    cursor: pointer;
    border-bottom: 1px solid black;
    text-align: center;
  }
  .option:hover {
    /*text-decoration: underline;*/
    color: rgba(255,255,255,1);
    background-color: rgba(50, 48, 52, 1)
  }
  .fade-enter-active {
    transition: opacity .5s;
  }
  [active=true]{
    background-color: #19181A;
  }
</style>
