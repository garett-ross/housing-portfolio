<template>
  <div class="query-form">
    <form @submit.prevent="submitQuery">
      <div v-for="(filter, index) in filters" :key="index" class="filter-row">
        <select v-model="filter.field">
          <option value="price">Price</option>
          <option value="date">Date</option>
          <!-- Add more options here -->
        </select>
        <select v-model="filter.operator">
          <option value="eq">Equals</option>
          <option value="ne">Not Equals</option>
          <option value="gt">Greater Than</option>
          <option value="lt">Less Than</option>
          <!-- Add more operators here -->
        </select>
        <input v-model="filter.value" type="text" placeholder="Value" />
        <button @click.prevent="removeFilter(index)">Remove</button>
      </div>
      <button type="button" @click="addFilter">Add Filter</button>
      <button type="submit">Submit</button>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      filters: [{ field: '', operator: 'eq', value: '' }]
    };
  },
  methods: {
    addFilter() {
      this.filters.push({ field: '', operator: 'eq', value: '' });
    },
    removeFilter(index) {
      this.filters.splice(index, 1);
    },
    submitQuery() {
      this.$emit('submit-query', this.filters);
    }
  }
};
</script>

<style scoped>
.query-form {
  margin-bottom: 20px;
}
</style>
