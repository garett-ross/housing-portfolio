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
      <QueryBox
        v-for="(box) in queryBoxes"
        :key="box.id"
        :id="box.id" 
        @delete-query="deleteQueryBox"
      />
      <button class="add-query-box" @click="addQueryBox">Add A New Query</button>
    </div>
    <div class="footer">
      <ul class="socials">
      <li class="social"><a href="https://www.linkedin.com/in/garett-ross/">LinkedIn</a></li>
      <li class="social"><a href="https://github.com/garett-ross">GitHub</a></li>
      </ul>
      <br>
      <p class="attribution">Price Paid data copyright HM Government, published for educational purposes under the Open Govenment Licence</p>
      
    </div>
  </div>
</template>

<script>
import QueryBox from './components/QueryBox.vue';
import { v4 as uuid } from 'uuid';

export default {
  components: {
    QueryBox,
  },
  data() {
    return {
      queryBoxes: [{ id: uuid() }], // Initialize with one query box with a unique ID
    };
  },
  methods: {
    addQueryBox() {
      this.queryBoxes.push({ id: uuid() }); // Push a new object with a unique ID for each new query box
    },
    // Delete query box by its ID
    deleteQueryBox(id) {
      // Filter out the box with the given id
      this.queryBoxes = this.queryBoxes.filter(box => box.id !== id);
    },
  },
};
</script>

<style scoped>
/* Styling is unchanged */
html, body {
  height: 100%;
  margin: 0;
  padding: 0;
  background-color: black !important;
  color: white !important;
}

.footer {
  display: flex;
  flex-direction: column;
  align-items: center; /* Centers content horizontally */
  text-align: center; /* Center text */
  padding: 5%; /* Adjust padding for better balance */
}

.socials {
  list-style: none;
  display: flex;
  gap: 20px; /* Use a smaller gap to evenly space links */
  padding: 0;
  margin: 0;
}

.attribution {
  margin-top: 10;
}

.hero {
  width: 100%;
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
