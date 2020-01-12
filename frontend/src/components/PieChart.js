import axios from "axios"
import { Doughnut } from "vue-chartjs";

export default {
  name: "PieChart",
  extends: Doughnut,
  props: {
    type: String
  },
  data: function () {
    return {
      chartData: {},
      chartOptions: {
        responsive: true,
        cutoutPercentage: 40,
        maintainAspectRatio: false
      }
    };
  },
  mounted: function () {
    let endpointStr = "http://localhost:5000/api/";
    let emailStr = "email=john.doe@gmail.com";

    if (this.type === "assets") {
      // run get requests for the asset information
      axios
        .get(endpointStr + "get_assets?" + emailStr)
        .then(resp => {
          if (resp.data !== null) {
            this.chartData = {
              labels: ["Cash", "Use", "Invested"],
              datasets: [
                {
                  backgroundColor: ["#41B883", "#E46651", "#cc65fe"],
                  data: [
                    resp.data["cash"].toFixed(2),
                    resp.data["use"].toFixed(2),
                    resp.data["invested"].toFixed(2)
                  ]
                }
              ]
            }
            // only render after the data has been received
            this.renderChart(this.chartData, this.chartOptions);
          }
        })
        .catch(error => {
          // log to the console
          // Todo: Handle this better
          console.error(error);
        });
    } else if (this.type === "liabilities") {
      // run get requests for the asset information
      axios
        .get(endpointStr + "get_liabilities?" + emailStr)
        .then(resp => {
          if (resp.data !== null) {
            this.chartData = {
              labels: ["Current", "Long"],
              datasets: [
                {
                  backgroundColor: ["#41B883", "#E46651"],
                  data: [
                    resp.data["current"].toFixed(2),
                    resp.data["long"].toFixed(2)
                  ]
                }
              ]
            }
            // only render after the data has been received
            this.renderChart(this.chartData, this.chartOptions);
          }
        })
        .catch(error => {
          // log to the console
          // Todo: Handle this better
          console.error(error);
        });
    } else {
      throw Error("Unknown type input");
    }
  },
  methods: {
    getUserData: function () {
      // Todo: make request to the backend to get data based on type

    }
  }
};