<template>
  <div class="query-box">
    <form @submit.prevent="submitQuery">
      <!-- Delete button emits delete-query event -->
      <button class="delete-query" @click.prevent="deleteSelf">Delete Query</button>

      <div v-for="(filter, index) in filters" :key="index" class="filter-row">
        <!-- Attributes drop-down -->
        <select v-model="filter.field" @change="getUniqueValues(filter.field, index)">
          <option value="price">Price</option>
          <option value="date">Date</option>
          <option value="postcode">Postcode</option>
          <option value="type">Type of Building</option>
          <option value="old_new">Old or New</option>
          <option value="duration">Leasehold or Freehold</option>
          <option value="street">Street</option>
          <option value="locality">Locality</option>
          <option value="town_city">Town or City</option>
          <option value="district">District</option>
          <option value="county">County</option>
        </select>

        <!-- Operator selection for price and date fields -->
        <select v-if="['price', 'date'].includes(filter.field)" v-model="filter.operator">
          <option value="eq">Equals</option>
          <option value="ne">Not Equals</option>
          <option value="gt">Greater Than</option>
          <option value="lt">Less Than</option>
          <option value="ge">Greater Than or Equal To</option>
          <option value="le">Less Than or Equal To</option>
        </select>

        <!-- Filter options -->
        <select v-if="filter.options.length && !isFreeTextFilter(filter.field)" v-model="filter.value">
          <option v-for="option in filter.options" :key="option" :value="option">{{ option }}</option>
        </select>


        <input v-if="filter.field === 'date'" v-model="filter.value" type="date" />


        <input v-if="filter.field === 'price'" v-model="filter.value" type="text" placeholder="Enter Price" />

        <button @click.prevent="removeFilter(index)">Remove</button>
      </div>
      <div class="buttons">
        <button type="button" @click="addFilter">Add Filter</button>
        <button type="submit">Get Data</button>
      </div>
    </form>

    <div v-if="averages.length > 0">
      <h3>Filtered Data Chart</h3>
      <div ref="chart"></div>
    </div>
  </div>

</template>

<script>
import { nextTick } from 'vue';
import Plotly from 'plotly.js-dist';

export default {
  props: {
    id: String
  },
  data() {
    return {
      filters: [],
      averages: [] // To store monthly averages
    };
  },
  methods: {
    isFreeTextFilter(field) {
      return field === 'price' || field === 'date';
    },

    async getUniqueValues(field, filterIndex) {
      const activeFilters = this.filters.slice(0, filterIndex).reduce((acc, filter) => {
        if (filter.field && filter.value) {
          acc[filter.field] = filter.value;
        }
        return acc;
      }, {});

      try {
        const response = await fetch('/unique', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ db_header: field, filters: activeFilters }),
        });

        const data = await response.json();
        this.filters[filterIndex].options = data;
      } catch (error) {
        console.error('Error fetching unique values:', error);
      }
    },

    addFilter() {
      this.filters.push({ field: '', operator: 'eq', value: '', options: [] });
    },

    removeFilter(index) {
      this.filters.splice(index, 1);
    },
    
    deleteSelf() {
      this.$emit('delete-query', this.id);
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

      const isEmptyQuery = Object.keys(query).length === 0;

      if (isEmptyQuery) {
        fetch('/api', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          },
        })
          .then(response => response.json())
          .then(data => {
            this.processData(data);
          })
          .catch(error => {
            console.error('Error fetching data (GET request):', error);
          });
      } else {
        fetch('/api', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(query),
        })
          .then(response => response.json())
          .then(data => {
            this.processData(data);
          })
          .catch(error => {
            console.error('Error fetching data (POST request):', error);
          });
      }
    },

    processData(data) {
      const resampledData = this.groupByMonth(data);
      this.averages = this.calculateAverages(resampledData);

      nextTick(() => {
        this.renderChart();
      });
    },

    groupByMonth(data) {
      return data.reduce((acc, item) => {
        const date = new Date(item.date);
        const month = `${date.getFullYear()}-${(date.getMonth() + 1).toString().padStart(2, '0')}`;
        if (!acc[month]) {
          acc[month] = [];
        }
        acc[month].push(item.price);
        return acc;
      }, {});
    },

    calculateAverages(groupedData) {
      return Object.keys(groupedData).map(month => {
        const prices = groupedData[month];
        const sum = prices.reduce((total, price) => total + price, 0);
        const avg = sum / prices.length;
        return { month, averagePrice: avg };
      });
    },

    renderChart() {
      if (this.averages && this.averages.length > 0) { 
        const layout = {
          grid: { rows: 2, columns: 1, pattern: 'independent' },
          xaxis: { title: 'Month' },  // X-axis title for scatter plot
          yaxis: { title: 'Average Price' },  // Y-axis title for scatter plot
          xaxis2: { title: 'Price' },  // X-axis title for histogram
          yaxis2: { title: 'Count' },  // Y-axis title for histogram
          height: 600,
          title: 'Price Analysis',
        };

        // Scatter plot trace for average prices over time
        const scatter = {
          x: this.averages.map(item => item.month),
          y: this.averages.map(item => item.averagePrice),
          type: 'scatter',
          mode: 'markers',
          name: 'Average Price',
          xaxis: 'x',  // Uses the default x-axis (xaxis)
          yaxis: 'y',  // Uses the default y-axis (yaxis)
        };

        // Histogram trace for price distribution
        const histogram = {
          x: this.averages.map(item => item.averagePrice),  // Use averagePrice for the histogram
          type: 'histogram',
          name: 'Price Distribution',
          xaxis: 'x2',  // Assign to the second x-axis (xaxis2)
          yaxis: 'y2',  // Assign to the second y-axis (yaxis2)
        };

        // Combine traces into a single data array
        const data = [scatter, histogram];

        // Render the plot using Plotly
        Plotly.newPlot(this.$refs.chart, data, layout);
      }
    }

  }
};
</script>

<style scoped>
.query-box {
  margin-top: 10px;
  border: 2px solid rgb(44, 107, 190);
}
.filter-row {
  margin-bottom: 10px;
  padding: 0px;
  flex: 0%;
}

.buttons {
  display: flex;
  margin: 0%;
  padding: 0;
  justify-content: flex-start;
}
input[type="text"], input[type="date"], select {
  margin-right: 10px;
}
button {
  margin-top: 0px;
  margin-right: 10px;
}

.delete-query {
  position: relative;
  left: 86%;
  margin-top: 0px;
  margin-right: 20px;
}
</style>
