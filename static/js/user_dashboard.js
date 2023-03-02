function displayPerformanceChart(username, performanceData) {
    var ctx = document.getElementById(username + "-performance-chart").getContext("2d");
    var data = {
      labels: performanceData[username].map(function(performance) {
        return performance.date;
      }),
      datasets: [
        {
          label: username,
          data: performanceData[username].map(function(performance) {
            return performance.score;
          }),
          backgroundColor: "rgba(255, 99, 132, 0.2)",
          borderColor: "rgba(255,99,132,1)",
          borderWidth: 1,
        },
      ],
    };
    var options = {
      scales: {
        yAxes: [
          {
            ticks: {
              beginAtZero: true,
              max: 100,
            },
          },
        ],
      },
    };
    var chart = new Chart(ctx, {
      type: "line",
      data: data,
      options: options,
    });
  }
  