const question_graph_data = JSON.parse(unescapeHtml(document.getElementById('question_graph_data').textContent));

/**
  * 円グラフ自体にラベルを追加するプラグイン
  * dataString の部分で表示するラベルを変更可能
  */
const dataLabelPlugin = Chart.plugins.register({
    afterDatasetsDraw: (chart, easing) => {
        const ctx = chart.ctx;
        ctx.fillStyle = '#ffffff';
        const padding = 5;
        const fontSize = WINDOW_WIDTH < 768 ? 6 : 17;
        const fontStyle = 'normal';
        const fontFamily = 'Helvetica Neue';
        for (const [i, dataset] of chart.data.datasets.entries()) {
            ctx.font = Chart.helpers.fontString(fontSize, fontStyle, fontFamily);
            let dataSum = 0;
            for (const dataset of chart.data.datasets) {
                dataSum = dataset.data.reduce((prev, current) => (prev + current));
            }
            meta = chart.getDatasetMeta(i);
            if (!meta.hidden) {
                for (const [index, element] of meta.data.entries()) {
                    // var dataString = chart.data.labels[index] ラベルにする場合
                    const dataString = (Math.round(dataset.data[index] / dataSum * 100 * 10)/10).toString() + "%";
                    ctx.textAlign = 'center';
                    ctx.textBaseline = 'middle';
                    const position = element.tooltipPosition();
                    ctx.fillText(dataString, position.x, position.y - (fontSize / 2) - padding);
                }
            }
        }
    }
});

/**
 * 渡された data からドーナツチャートを生成する。
 * @param {Object} doughnuts_chart_data チャート作成に使用する色・ラベル等のデータ
 * @param {String} canvas_id 図を描画する要素のid名
 */
const renderDoughnutChart = (doughnuts_chart_data, canvas_id) => {
    const canvas = $(`#${canvas_id}`);
    const sum = doughnuts_chart_data.data.datasets[0].data.reduce(function (accumulator, currentValue) {
        return accumulator + currentValue;
    }, 0);

    // 回答がある場合とない場合を分岐
    if (sum === 0) {
        canvas.closest(".question-chart").html(NOCHOICE);
    } else {
        new Chart(canvas[0].getContext('2d'), doughnuts_chart_data);
    }
};

/**
 * 設問から設問に紐づく回答を絞り込み、円グラフを生成するためのデータを作成し、
 * loadDoughnutChart() にデータを渡す。
 * @param {Object} graph_data グラフを作成する質問情報
 */
const createDoughnutsChartData = (graph_data) => {
    const doughnuts_chart_data = {
        datasets: [{
            data: graph_data.data,
            backgroundColor: HV_COLORS,
            hoverBackgroundColor: HV_COLORS,
            plugins: [dataLabelPlugin],
        }],
        labels: graph_data.labels
    };
    return {
        type: 'doughnut',
        data: doughnuts_chart_data,
        options: {
            legend: { position: 'right' }
        }
    };
};


/**
 * 設問から設問に紐づく回答を絞り込み、ランキングを作成する
 * @param {Object} question ランキングを作成するの質問情報
 * @param {Number} index 質問ID(DB: Question)
 */
const createQuestionChart = (question, index) => {
    // 最新回答5件
    const current_choices = createCurrentChoices(question.graph_data.time);
    // 良いね上位5件
    const liked_choices = createLikeTop5(question.graph_data.like);
    const choice_chart = `<div id="question-${index}" class="questions-list">
            <ul class="nav nav-tabs" id="rank-tab-list-${index}">
                <li class="active"><a href="#like-${index}" data-toggle="tab">
                    ${document.getElementById('like_tabtitle').innerText}</a>
                </li>
                <li>
                    <a href="#current-${index}" data-toggle="tab">${document.getElementById('current_tabtitle').innerText}</a>
                </li>
            </ul>
            <div class="tab-content tab-container" id="rank-tab-content-${index}">
                <div class="tab-pane active" id="like-${index}"><div>${liked_choices}</div></div>
                <div class="tab-pane" id="current-${index}"><div>${current_choices}</div></div>
            </div>
        </div>`;
    return question.graph_data.like.length === 0 && question.graph_data.time.length === 0 ? NOCHOICE : choice_chart;

};

/**
 * 設問に紐づく回答の最新5件の回答を引数に取り、タグの文字列で返却する。
 * @param {Array} choice_time_data 回答と回答時間のデータ
 * @return {String}
 */
const createCurrentChoices = (choice_time_data) => {
    const current_choice_list = [];
    for (const choice_data of choice_time_data) {
        const timestamp = moment(choice_data.time);
        current_choice_list.push(`
            <div class="choice-box">
                <div class="date-box">
                    <p class="month-text">${timestamp.format("MMMM")}</p>
                    <p class="day-text">${timestamp.format("DD")}</p>
                </div>
                <p class="date-text">${timestamp.format("YYYY/MM/DD HH:mm:ss")}<br>
                    <span class="choice-text">${choice_data.text}</span>
                </p>
            </div>
        `)
    }
    return current_choice_list.join("");
};

/**
 * 設問に紐づく回答のイイネ数上位5件を引数に取り、タグの文字列で返却する。
 * @param {Array} choice_liked_data 回答といいね数のデータ
 * @return {String}
 */
const createLikeTop5 = (choice_liked_data) => {
    const liked_choice_list = [];
    for (const choice of choice_liked_data) {
        const timestamp = moment(choice.timestamp).format("YYYY/MM/DD HH:mm:ss");
        liked_choice_list.push(`
            <div class="choice-box">
                <div class="date-box">
                    <p class="month-text">LIKE</p>
                    <p class="day-text">${choice.like}</p>
                </div>
                <p class="date-text">${timestamp}<br>
                    <span class="choice-text">${choice.text}</span>
                </p>
            </div>
        `)
    }

    return liked_choice_list.join("");
};

const choice_list = document.getElementById('choices');
question_graph_data.forEach((q, index) => {
    switch (q.type) {
        case "selection": // 選択肢の中から１つ、もしくは複数を選択する設問
            const single_list = document.createElement('li');
            const doughnuts_chart_data = createDoughnutsChartData(q.graph_data);
            const canvas_id = `doughnuts_chart-${index}`;
            single_list.innerHTML = `<h4>${q.question_text}</h4>
                <div id="question-${index}" class="question-chart">
                    <canvas id="${canvas_id}"></canvas>
                </div>`;
            choice_list.appendChild(single_list);
            renderDoughnutChart(doughnuts_chart_data, canvas_id);
            break;
        case "open_end": // 設問に対して自由記述で回答可能な設問
            const question_list = document.createElement('li');
            question_list.innerHTML = `<h4>${q.question_text}</h4>` + createQuestionChart(q, index);
            choice_list.appendChild(question_list);
            break;
    }
});
