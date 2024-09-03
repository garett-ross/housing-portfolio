<template>
  <div class="query-form">
    <h2>Query Form</h2>
    <form @submit.prevent="submitQuery">
      <div v-for="(filter, index) in filters" :key="index" class="filter-row">
        <!-- Dropdown for selecting the field -->
        <select v-model="filter.field">
          <option value="price">Price</option>
          <option value="date">Date</option>
          <option value="postcode">Postcode</option>
          <option value="type">Type</option>
          <option value="old_new">Old or New</option>
          <option value="duration">Freehold or Leasehold</option>
          <option value="street">Street</option>
          <option value="locality">Locality</option>
          <option value="town_city">Town or City</option>
          <option value="district">District</option>
          <option value="county">County</option>
        </select>
        <select v-model="filter.operator">
          <option value="eq">Equals</option>
          <option value="ne">Not Equals</option>
          <option value="gt">Greater Than</option>
          <option value="lt">Less Than</option>
          <option value="ge">Greater Than or Equal To</option>
          <option value="le">Less Than or Equal To</option>
        </select>
        <input
          v-model="filter.value"
          type="text"
          placeholder="Value"
        />
        <button @click="removeFilter(index)">Remove</button>
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
      filters: [
        { field: '', operator: 'eq', value: '' }
      ]
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
      const query = this.filters.reduce((acc, filter) => {
        if (filter.field && filter.value !== '') {
          acc[filter.field] = {
            operator: filter.operator,
            value: filter.value
          };
        }
        return acc;
      }, {});

      // Send the query to the API
      fetch('http://localhost:5000/api', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(query)
      })
      .then(response => response.json())
      .then(data => {
        console.log('Response:', data);
      })
      .catch(error => {
        console.error('Error:', error);
      });
    }
  }
};
</script>

<style scoped>
.query-form {
  max-width: 600px;
  margin: auto;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 5px;
}

.filter-row {
  margin-bottom: 10px;
}

input[type="text"] {
  margin-right: 10px;
}

button {
  margin-top: 10px;
}
</style>
