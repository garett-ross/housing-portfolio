<template>
  <div class="app-container">
    <!-- Hero/Banner Section -->
    <div class="hero">
      <h1>Property Data Analysis</h1>
      <p>Explore property data with custom queries and visualizations.</p>
    </div>

    <!-- Introductory Text -->
    <div class="intro">
      <p>Use the form below to filter property data by various criteria, such as price, date, and location. You can also add multiple queries to compare different data sets.</p>
    </div>
    <!-- Query Boxes Section -->
    <div class="query-boxes">
      <QueryBox v-for="(box, index) in queryBoxes" :key="index" @remove="removeQueryBox(index)" />
      <button class="add-query-box" @click="addQueryBox">Add Query Box</button>
    </div>
  </div>
</template>

<script>

import QueryBox from './components/QueryBox.vue';

export default {
  components: {
    QueryBox
  },
  data() {
    return {
      queryBoxes: [1], // Initially one query box
    };
  },
  methods: {
    addQueryBox() {
      this.queryBoxes.push(this.queryBoxes.length + 1);
    },
    removeQueryBox(index) {
      this.queryBoxes.splice(index, 1);
    }
  }
};
</script>

<style scoped>
/* Ensure body and html take full height and remove default margins */
html, body {
  height: 100%;
  margin: 0;
  padding: 0;
  background-color: black !important;
  color: white !important;
}


/* Hero/Banner Section */
.hero {
  width: 100%;
  background-image: url('path-to-your-banner-image.jpg');
  background-size: cover;
  background-position: center;
  color: white;
  text-align: center;
  padding: 60px 20px;
}

.hero h1 {
  font-size: 2.5rem;
  margin: 0;
}

.hero p {
  font-size: 1.25rem;
  margin: 10px 0 0;
}

/* Introductory Text */
.intro {
  text-align: center;
  margin: 20px auto;
  max-width: 800px;
  font-size: 1.1rem;
}

/* Query Boxes Section */
.query-boxes {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  border: 2px;
  border-color: red;
}

.query-box {
  width: 100%;
  max-width: 1000px;
  margin: 10px 0;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  background-color: rgb(59, 53, 53);
  border-radius: 5px;
}

.add-query-box {
  margin-top: 20px;
  padding: 10px 20px;
  font-size: 1rem;
  cursor: pointer;
}




</style>
