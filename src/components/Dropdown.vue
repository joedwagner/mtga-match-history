<template>
  <select>
    <option v-for="option in options">{{ option }}</option>
  </select>
</template>

<script>
  export default {
    name: 'dropdown',
    props: {
      options: {
        type: Array,
        required: true  
      }
    }
  }
</script>

<style scoped>

</style>
