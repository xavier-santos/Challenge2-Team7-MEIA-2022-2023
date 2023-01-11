<template>
  <div>
    <div class="header">
      <h1>Maintenance Scheduling</h1>
      <p>MEIA - Team 7</p>
    </div>
    <ScheduleChart />
  </div>
</template>

<script>
import ScheduleChart from "./components/ScheduleChart.vue";

export default {
  name: "App",
  components: {
    ScheduleChart,
  },
};
</script>

<style>
body {
  margin: 0px;
}
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
.header {
  padding: 1px;
  text-align: center;
  background: #2c3e50;
  color: white;
}
h1{
  font-size: 50px;
}
p{
  font-size: 30px;
}
</style>
