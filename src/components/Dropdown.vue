<template>
  <div class="d-container" v-click-outside="closeDropdown">
        <div class="selectedOptionBox" v-on:click="toggleDropdown">
          <span class="label">{{ capitalizedLabel +':' }}</span>
          <span class="selectedOption" v-model="selectedOption">{{ selectedOption }}</span>
          <div v-bind:class="{upArrow: true, downArrow: dropdownOpen }"></div>
        </div>
        <div class="dropdown" v-show="dropdownOpen">
          <ul>
            <li class="listOption" v-for="option in options" v-on:click="selectedOption = option; closeDropdown(); updateFilter()">{{ Array.isArray(options) ? option : option.name }}<div class="checkmark" v-show="selectedOption === option">&#x1F5F8;</div></li>
        </ul>
      </div>
  </div>
</template>

<script>
  import ClickOutside from 'vue-click-outside'
  export default {
    name: 'dropdown',
    directives: {
      ClickOutside
    },
    props: {
      options: {
        type: [Array, Object],
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
        dropdownOpen: false
      }
    },
    computed: {
      capitalizedLabel() {
        return this.label.substring(0,1).toUpperCase() + this.label.slice(1) 
      }
    },
    methods: {
      toggleDropdown () {
        this.dropdownOpen = !this.dropdownOpen
      },
      closeDropdown () {
        this.dropdownOpen = false
      },
      updateFilter() {
        this.$emit('update-filter', {type: 'timeframe', filter: this.selectedOption})
      }
    }
  }
</script>

<style scoped>
  .d-container {
    position: relative;
    display: inline-block;
    vertical-align: middle;
    font-size: .9em
  }
  .selectedOptionBox {
    background-color: #19181A;
    display: inline-block;
    padding-top: .5em;
    padding-bottom: .5em;
    width: 100%;
  }
  .upArrow {
    width: 0;
    border: 5px solid;
    border-color: transparent;
    border-top-color: white;
    position: absolute;
    right: 10px;
    top: 1em;
  }
  .downArrow {
    border-top-color: transparent;
    border-bottom-color: white;
    top: .5em;
  }
  .dropdown {
    background-color: #19181A;
  }
  ul {
    width: 100%;
    list-style: none;
    position: absolute;
    z-index: 999;
    display: flex;
    flex-direction: column;
    vertical-align: middle;
    padding-left: 0;
    margin: 0;
    background-color: inherit;
  }
  ul > li {
    display: block;
    padding: .5em;
  }
  .listOption {
    display: block;
    padding: .5em;
  }
  ul > li:hover {
    background-color: rgba(50, 48, 52, 1);
  }
  .label {
    padding: .5em;
  }
  .checkmark {
    display: inline-block;
    position: absolute;
    right: 10px;
  }
</style>