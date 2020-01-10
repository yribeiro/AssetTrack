<template>
  <div id="app">
    <!-- NavBar Div -->
    <div>
      <b-navbar toggleable="lg" type="dark" variant="dark">
        <b-navbar-brand href="#">
          <!-- <img src="./assets/logo.png" width="65%" /> -->
          <!-- TODO: Insert valid icon -->
        </b-navbar-brand>

        <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

        <b-collapse id="nav-collapse" is-nav>
          <!-- Right aligned nav items -->
          <b-navbar-nav class="ml-auto">
            <b-nav-item href="#" right>Sign Out</b-nav-item>
          </b-navbar-nav>
        </b-collapse>
      </b-navbar>
    </div>
    <!-- Main Section -->
    <Dashboard msg="Welcome to the AssetTrack Dashboard" />
    <div class="footer mt-5">
      <div class="container">
        <span class="text-muted">AssetTrack Creator Yohahn Ribeiro 2019 (c)</span>
      </div>
    </div>
  </div>
</template>

<script>
import Dashboard from "./components/Dashboard.vue";

export default {
  name: "app",
  components: {
    Dashboard
  }
};
</script>

<style>
#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

.footer {
  width: 100%;
  height: 60px; /* Set the fixed height of the footer here */
  line-height: 60px; /* Vertically center the text there */
  background-color: #f5f5f5;
}

.container {
  width: auto;
  max-width: 680px;
  padding: 0 15px;
}
</style>
