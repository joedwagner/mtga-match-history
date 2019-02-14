<template>
  <div>
    <label>{{ label }}</label>
    <select v-model="selectedOption" v-on:change="passFilter">
      <option v-for="option in options">{{ option }}</option>
    </select>
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
        selectedOption: this.options[0]
      }
    },
    methods: {
      passFilter() {
        let filter = {}
        if (this.selectedOption === 'All') {
          filter = null
        } else {
          filter.filterType = this.label.toLowerCase(),
          filter.filterValue = this.selectedOption
        }
        this.$emit('filter-changed', filter)
      }
    }
  }
</script>

<style scoped>

</style>
