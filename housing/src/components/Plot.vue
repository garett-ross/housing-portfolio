<template>
  <div>
    <form @submit.prevent="fetchData">
      <!-- Example form to submit filters -->
      <input v-model="filters.price" placeholder="Price" />
      <input v-model="filters.town_city" placeholder="Town/City" />
      <button type="submit">Submit</button>
    </form>

    <div ref="plot" style="width:100%; height:400px;"></div>
  </div>
</template>

<script>
import Plotly from 'plotly.js-dist';

export default {
  data() {
    return {
      filters: {
        price: '',
        town_city: ''
      },
      plotData: []
    };
  },
  methods: {
    fetchData() {
      // Construct the query based on the filters
      const query = {};
      if (this.filters.price) {
        query.price = { operator: 'eq', value: this.filters.price };
      }
      if (this.filters.town_city) {
        query.town_city = { operator: 'eq', value: this.filters.town_city };
      }

      // Fetch data from the API
      fetch('http://localhost:5000/api', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(query)
      })
        .then(response => response.json())
        .then(data => {
          this.plotData = data;
          this.createPlot();
        })
        .catch(error => {
          console.error('Error fetching data:', error);
        });
    },
    createPlot() {
      // Extract data for plotting
      const x = this.plotData.map(item => item.date);  // Example: x-axis is the date
      const y = this.plotData.map(item => item.price); // Example: y-axis is the price

      const trace = {
        x: x,
        y: y,
        mode: 'lines+markers',
        type: 'scatter'
      };

      const layout = {
        title: 'Price vs Date',
        xaxis: { title: 'Date' },
        yaxis: { title: 'Price' }
      };

      Plotly.newPlot(this.$refs.plot, [trace], layout);
    }
  }
};
</script>

<style scoped>
/* Add your styles here */
</style>
