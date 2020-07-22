const respondent_transition_data = JSON.parse(unescapeHtml(document.getElementById('respondent_transition_data').textContent));

/**
 * バックエンドから送られたデータを元に折れ線グラフを生成する。
 */
const loadCharts = () => {
  const chartDataSet = {
    type: 'line',
    data: {
      labels: respondent_transition_data.labels,
      datasets: [{
        label: transition,
        data: respondent_transition_data.values,
        backgroundColor: 'rgba(155, 232, 0, 0.3)',
        borderColor: 'rgb(155, 232, 0)',
        lineTension: 0,
      }]
    },
    options: {
      scales: {
        yAxes: [{
        type: 'linear',
        ticks: {
          beginAtZero: true,
          userCallback: function (label, index, labels) {
            if (Math.trunc(label) === label) {
              return label;
            }
          }
        }
      }]
    },
    }
  };

  const ctx = document.getElementById("line_chart").getContext('2d');
  ctx.canvas.parentNode.style.width = '80%';
  new Chart(ctx, chartDataSet);

};

loadCharts();
