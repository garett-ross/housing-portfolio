<template>
  <div class="query-box">
    <form @submit.prevent="submitQuery"> <!-- prevent reloading entire page -->
      <!-- option to remove query box -->
      <!-- used click.prevent to stop it trying to call the api when deleted -->
      <button class="delete-query" @click.prevent="deleteSelf()">Delete Query</button>
      <!-- multiple filters can be applied to each query, show options for each -->
      <div v-for="(filter, index) in filters" :key="index" class="filter-row">
        <!-- attributes drop-down -->
        <select v-model="filter.field">
          <option value="price">Price</option>
          <option value="date">Date</option>
          <option value="postcode">Postcode</option>
          <option value="town_city">Town or City</option>
          <option value="county">County</option>
        </select>
        <!-- operator options -->
        <select v-model="filter.operator">
          <option value="eq">Equals</option>
          <option value="ne">Not Equals</option>
          <option value="gt">Greater Than</option>
          <option value="lt">Less Than</option>
          <option value="ge">Greater Than or Equal To</option>
          <option value="le">Less Than or Equal To</option>
        </select>
        <!-- value as free text - can this be variable? -->
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
    <div v-if="averages.length > 0">
      <h3>Filtered Data Chart</h3>
      <div ref="chart"></div>
    </div>
  </div>
</template>

<script>
import Plotly from 'plotly.js-dist';
import { nextTick } from 'vue';

function groupByMonth(data) {
  const groupedData = data.reduce((acc, item) => {
    const date = new Date(item.date);
    const month = `${date.getFullYear()}-${(date.getMonth() + 1).toString().padStart(2, '0')}`;
    if (!acc[month]) {
      acc[month] = [];
    }
    acc[month].push(item.price);
    return acc;
  }, {});
  return groupedData;
}

function monthlyAverages(groupedData) {
  return Object.keys(groupedData).map(month => {
    const prices = groupedData[month];
    const sum = prices.reduce((total, price) => total + price, 0);
    const avg = sum / prices.length;
    return { month, averagePrice: avg };
  });
}

export default {
  props: {
    index: Number // index in parent array
  },
  data() {
    return {
      filters: [{ field: '', operator: 'eq', value: '' }],
      chartData: [],
      averages: []
    };
  },
  methods: {
    deleteSelf() {
      this.$emit('delete-query', this.index)
    },
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
            value: filter.value,
          };
        }
        return acc;
      }, {});

      fetch('http://localhost:5000/api', { // adjust the URL in production if necessary
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(query)
      })
      .then(response => response.json())
      .then(data => {
        const resampledData = groupByMonth(data);
        this.averages = monthlyAverages(resampledData);

        // Ensure the DOM is updated before rendering the chart
        nextTick(() => {
          this.renderChart();
        });
      })
      .catch(error => {
        console.error('Error fetching data:', error);
      });
    },
    renderChart() {
      if (this.averages && this.averages.length > 0) {
        const layout = {
          title: 'Filtered Data',
          xaxis: { title: 'Date' },
          yaxis: { title: 'Price' }
        };

        const plotData = [
          {
            x: this.averages.map(item => item.month),
            y: this.averages.map(item => item.averagePrice),
            type: 'scatter',
            mode: 'markers'
          }
        ];

        Plotly.newPlot(this.$refs.chart, plotData, layout);
      }
    }
  }
};
</script>

<style scoped>
.query-box {
  margin-top: 10px;
  border: 2px solid red; /* Changed to 'solid' for visibility */
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

/* this is a bit awkward */
.delete-query {
  position: relative;
  left: 86%;
  margin-top: 0px;
  margin-right: 20px;
}
</style>
