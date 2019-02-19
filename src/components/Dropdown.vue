<template>
  <label>{{ label }}
    <span class="thing">
      <select>
        <option v-for="option in options">{{ option }}</option>
      </select>
    </span>
  </label>
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
  .thing {
    position: relative;
    display: inline-block;
    vertical-align: middle; 
  }
  select {
    -webkit-appearance: none;
    border: 0;
    padding: .5em;
    padding-right: 2.5em;
    font-size: .9em;
    margin: 0;
    background-color: #19181A;
    color: rgba(255,255,255,.9);
  }
  .thing::before, .thing::after {
    content: "";
    position: absolute;
    pointer-events: none;
  }
  .thing::after {
    content: "\25BC";
    height: 1em;
    font-size: .625em;
    line-height: 1;
    right: 1.2em;
    top: 50%; 
    margin-top: -.5em;
  }
  .thing::before {
    width: 2em;
    right: 0;
    top: 0;
    bottom: 0;
    border-radius: 0 0px 0px 0;
    background-color: #19181A;
  }
  .thing:hover {
    background-color: rgba(50, 48, 52, 1);
  }
</style>
