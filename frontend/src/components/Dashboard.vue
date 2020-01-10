<template>
  <div class="dashboard">
    <b-container>
        <h3>{{ msg }}</h3>
    </b-container>
    <b-container class="mt-3">
        <b-row class="text-center">
            <b-col cols="8" class="border border-primary mr-2"> Test Chart Area </b-col>
            <b-col class="border border-primary"> Test Button and Net Worth Area </b-col>
        </b-row>
    </b-container>
    <b-container class="mt-3">
        <b-row class="text-center">
            <b-col class="border border-primary mr-2"> Pie Chart Area 1 </b-col>
            <b-col class="border border-primary"> Pie Chart Area 2 </b-col>
        </b-row>
    </b-container>
  </div>
</template>

<script>
export default {
  name: 'Dashboard',
  props: {
    msg: String
  }
}
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
</style>
