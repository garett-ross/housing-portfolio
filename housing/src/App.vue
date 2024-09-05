<!-- Main app code -->

<!-- HTML template for the app content -->
<template>
  <div class="app-container">

    <div class="hero">
      <h1>Property Data Analysis</h1>
      <p>Explore property data with custom queries and visualizations.</p>
    </div>

    <div class="intro">
      <p>Use the form below to filter property data by various criteria, such as price, date, and location. You can also add multiple queries to compare different data sets.</p>
    </div>

    <!-- Queries go here-->
    <div class="query-boxes">
      <QueryBox v-for="(box, index) in queryBoxes" :key="index" :index="index" @delete-query="deleteQueryBox"/>
      <button class="add-query-box" @click="addQueryBox">Add A New Query</button>
    </div>
  </div>
</template>

<!-- Script to provide interactivity-->
<script>

// import querybox component 
import QueryBox from './components/QueryBox.vue';

// get the query box class
export default {
  components: {
    QueryBox
  },
  data() {
    return {
      queryBoxes: [1], // create one query box initially
    };
  },

  methods: {
    addQueryBox() {
      this.queryBoxes.push(this.queryBoxes.length + 1);
    },
    // called from a click event within the query box component
    deleteQueryBox(index) {
      this.queryBoxes.splice(index, 1); // need to find specific box this has been called from!
    }
  }
};
</script>

<!-- styles for the main app-->
<style scoped>

html, body {
  height: 100%;
  margin: 0;
  padding: 0;
  background-color: black !important;
  color: white !important;
}



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


.intro {
  text-align: center;
  margin: 20px auto;
  max-width: 800px;
  font-size: 1.1rem;
}


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
