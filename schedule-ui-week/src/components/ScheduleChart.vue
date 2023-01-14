<template>
  <div>
    <g-gantt-chart
      v-for="weekday in scheduleData"
      :key="weekday.id"
      precision="hour"
      :chart-start="weekday.chartStart"
      :chart-end="weekday.chartEnd"
      :push-on-overlap="false"
      bar-start="myBeginDate"
      bar-end="myEndDate"
      color-scheme="vue"
      grid
    >
      <template #bar-tooltip="{ bar }">
        {{ bar.startHour }}-{{ bar.endHour }}: {{bar.ganttBarConfig.label}}
      </template>
      <g-gantt-row
        v-for="row in weekday.chartData"
        :key="row.id"
        :label="row.label"
        :bars="row.barList"
        :highlight-on-hover="true"
        bar-start="myStart"
        bar-end="myEnd"
      />
    </g-gantt-chart>
    <p>
      Please load the schedule file to see the engine maintenance for the next week
    </p>
    <input class="inputfile" type="file" v-on:change="onFileLoad" />
  </div>
</template>

<script>
import { reactive } from "vue";
import moment from "moment";

export default {
  name: "ScheduleChart",

  setup() {
    let inputFile;

    const chartDates = reactive({
      chartStart: "",
      chartEnd: "",
    });

    const scheduleData = reactive([]);

    const onFileLoad = async (e) => {
      var files = e.target.files || e.dataTransfer.files;
      if (!files.length) return;
      inputFile = files[0];
      inputFile = await readFile(inputFile);
      buildChart(inputFile);
    };

    const readFile = (file) => {
      var reader = new FileReader();
      reader.readAsText(file, "UTF-8");
      return new Promise(
        (resolve) =>
          (reader.onload = async function (evt) {
            var res = JSON.parse(evt.target.result);
            resolve(res);
          })
      );
    };

    const buildChart = (scheduleInput) => {
      const colors = ["#208AAE", "#9BC53D", "#C3423F"];



      scheduleInput.week_plan.forEach((weekday, i) => {

        var chartStart = getChartStart(i);

        getChartEnd(i);
        var weekdayData = [];

        weekday.workers_schedule.forEach((worker, i) => {
        var barList = [];
        worker.assigned_engines.forEach((task) => {
          var start = chartStart.clone().add(task.start_time, "hours");

          var taskStart = start.format("YYYY-MM-DD HH:mm");
          var taskStartHour = start.format("HH:mm");

          var taskEnd = start
            .clone()
            .add(task.maintenance_time, "hours")
            .format("YYYY-MM-DD HH:mm");

          var taskEndHour = start
            .clone()
            .add(task.maintenance_time, "hours")
            .format("HH:mm");

          if (taskStart < chartDates.chartStart) {
            chartDates.chartStart = start
              .clone()
              .subtract(1, "hours")
              .format("YYYY-MM-DD HH:mm");
          }

          if (taskEnd > chartDates.chartEnd) {
            chartDates.chartEnd = taskEnd;
          }

          var color = colors[worker.worker_id - 1];

          barList.push({
            myBeginDate: taskStart,
            myEndDate: taskEnd,
            startHour: taskStartHour,
            endHour: taskEndHour,
            worker: i,
            ganttBarConfig: {
              label: `Engine ${task.engine_id.toString()}`,
              id: task.engine_id,
              immobile: true,
              style: {
                background: color,
                borderRadius: "20px",
                color: "black",
              },
            },
          });
        });


        weekdayData.push({
          id: worker.worker_id,
          label: `Worker ${worker.worker_id.toString()}`,
          barList: barList,
        });
      });

        var indivualchartStart = chartDates.chartStart;

        var individualchartEnd = chartDates.chartEnd;

        scheduleData.push({
          chartData: weekdayData,
          chartStart: indivualchartStart,
          chartEnd: individualchartEnd,
          id: i
        });

      });

  
    };

    const getChartStart = (i) => {
      var start = moment().add(1, "week").day(i + 1).startOf("day");

      chartDates.chartEnd = start.format("YYYY-MM-DD HH:mm");

      return start;
    };

    const getChartEnd = (i) => {
      var end = moment().add(1, "week").day(i +1).endOf("day");

      chartDates.chartStart = end.format("YYYY-MM-DD HH:mm");

      return end;
    };

    return {
      chartDates,
      scheduleData,
      onFileLoad,
    };
  },
};
</script>
<style scoped>
p {
  color: black;
  font-weight: bold;
  font-size: 20px;
  margin-top: 40px;
}
</style>
