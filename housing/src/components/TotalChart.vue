<template>
  <div class="total-chart">
    <h2>Total Data Chart</h2>
    <div ref="chart"></div>
  </div>
</template>

<script>
import Plotly from 'plotly.js-dist';

export default {
  data() {
    return {
      chartData: []
    };
  },
  mounted() {
    this.fetchData();
  },
  methods: {
    fetchData() {
      fetch('http://localhost:5000/api', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json'
        }
      })
      .then(response => response.json())
      .then(data => {
        this.chartData = data;
        this.renderChart();
      })
      .catch(error => {
        console.error('Error fetching data:', error);
      });
    },
    renderChart() {
      if (this.chartData && this.chartData.length > 0) {
        const layout = {
          title: 'Total Data',
          xaxis: { title: 'Date' },
          yaxis: { title: 'Price' }
        };

        const plotData = [
          {
            x: this.chartData.map(item => item.date),
            y: this.chartData.map(item => item.price),
            type: 'scatter',
            mode: 'lines+markers'
          }
        ];

        Plotly.newPlot(this.$refs.chart, plotData, layout);
      }
    }
  }
};
</script>

<style scoped>
.total-chart {
  margin-bottom: 20px;
}
</style>
