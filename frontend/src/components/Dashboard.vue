<template>
  <div class="dashboard">
    <b-container>
      <h3>{{ msg }}</h3>
    </b-container>
    <hr>
    <b-container class="mt-3">
      <b-row class="text-center">
        <b-col cols="8" class="border border-secondary rounded mr-2">Test Chart Area</b-col>
        <b-col class="">
          <b-button size="lg" variant="info" id="updateButton">Update Portfolio</b-button>
          <div class="border border-secondary rounded mt-3" id="netWorth">
            <p class="mt-1">
              <b>Net Worth</b>
            </p>
            <h2 class="mt-1 mb-2">{{ currency }}{{ netWorth }}</h2>
          </div>
        </b-col>
      </b-row>
    </b-container>
    <hr>
    <b-container class="mt-4">
      <b-row class="text-center">
        <b-col class="border-right border-secondary mr-2">
          <h4 class="right">Your Assets</h4>
          <pie-chart :height="300"></pie-chart>
        </b-col>
        <b-col>
          <h4>Your Liabilities</h4>
          <pie-chart :height="300"></pie-chart>
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>
import axios from "axios";
import PieChart from "./PieChart.js";

export default {
  name: "Dashboard",
  components: { PieChart },
  props: {
    msg: String
  },
  data: function() {
    return {
      netWorth: "",
      currency: ""
    };
  },
  mounted: function() {
    // run the functions
    this.getNetWorth();
  },
  methods: {
    getNetWorth: function() {
      // make request to the backend
      axios
        .get("http://localhost:5000/api/get_net_worth?email=john.doe@gmail.com")
        .then(resp => {
          if (resp.data === null) {
            this.netWorth = "None";
            this.currency = "";
          } else {
            this.currency = "£";
            this.netWorth = resp.data.toFixed(2);
          }
        })
        .catch(error => {
          // log to the console
          console.error(error);
          this.netWorth = "Error";
        });
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}

#updateButton {
  width: inherit;
}
</style>
