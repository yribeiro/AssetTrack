import { Doughnut } from "vue-chartjs";

export default {
  name: "PieChart",
  extends: Doughnut,
  props: {},
  data: function () {
    return {
      chartData: {
        datasets: [
          {
            label: 'Data One',
            backgroundColor: ["#41B883", "#E46651"],
            data: [10, 20]
          }
        ]
      },
      chartOptions: {
        responsive: true,
        cutoutPercentage: 40,
        maintainAspectRatio: false
      }
    };
  },
  mounted: function () {
    // run the functions
    this.renderChart(this.chartData, this.chartOptions);
  },
  methods: {
    getUserData: function () {
      // Todo: make request to the backend to get data based on type
    }
  }
};