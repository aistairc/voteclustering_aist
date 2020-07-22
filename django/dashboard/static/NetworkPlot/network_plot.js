const area = document.getElementById('networkplot_area');
document.getElementById('area').style.height = WINDOW_WIDTH < WINDOW_HEIGHT ? CONTENT_HEIGHT/2 : CONTENT_HEIGHT;

var svg = d3.select("#area").attr("width", area.clientWidth).attr('height', area.clientHeight - 71),
    width = +svg.attr("width"),
    height = +svg.attr("height"),
    color = d3.scaleOrdinal(d3.schemeCategory20);
//movement define
//
 //  forceSimulation設定
var simulation = d3.forceSimulation()
    .force("link", d3.forceLink().id(function(d) { return d.id; }))
    .force("charge", d3.forceManyBody())
    //世界の中心に落ちていく力
    .force("center", d3.forceCenter(width / 2, height / 2))
  //  .force("center", velocityDecay(0.4))



// simulation.force("link")
//           .distance(function(){ return 10;})
//           .strength(function(){ return 2; })

// json読み込み
//
d3.json("/media/coffee_chiba_clustered_NWP.json", function(error, graph) {
  if (error) throw error;

  const links = [];
  var link = svg
    .append("g")
    .attr("class", "links")
    .selectAll("line")
    .data(graph.links)
    .enter().append("line")
    .attr("stroke-width", function(d) {
      links.push({source: d.source, text: d.text});
      return Math.sqrt(d.value);
    });

  var node = svg
    .append("g")
    .attr("class", "nodes")
    .selectAll("g")
    //change r size
    //d.r
//   .attr("r", function(d) { return int(d.dgree); })
    .data(graph.nodes)
    .enter()
    .append("g") ;

 // print(d.degree[1])
  const label_data = [];
  var circles = node.append("circle")
      .on("click", function(d){onClickCircle(d);})
      .attr("r", function(d){
     //    return 4*Math.sqrt(d.degree); } )
      if(d.degree == 1) { return 3 ; }
      else{ return 7*Math.log(d.degree);} } )
      .attr("fill", function(d) {
        label_data.push({
          id: d.id,
          group: d.group,
          text: d.text,
          color: color(d.group),
          links: []
        });
        return color(d.group);
      })
      .call(d3.drag()
          .on("start", dragstarted)
          .on("drag", dragged)
          .on("end", dragended));


  const label_area = document.getElementById('network_labels');
  const area_height = document.getElementById('content-wrapper').clientHeight - 70;
  label_area.style.height = `${area_height}px`;
  for (const d of label_data) {
    const links_data = links.filter(link => link.source == d.id)
    d.links = links_data
  }
  label_area.innerHTML = createLabelElements(label_data)

  var lables = node.append("text")
      .text(function(d) {
        return d.id;
      })
      .attr('x', 6)
      .attr('y', 3);
  node.append("title")
      .text(function(d) { return d.id; });

  simulation
      .nodes(graph.nodes)
      .on("tick", ticked);

  simulation.force("link")

      .links(graph.links);

  // simulation.velocityDecay(0.4)
  simulation.force("center", d3.forceCenter(width / 2, height / 2))

//  forceSimulation 描画更新用関数
  function ticked() {

    link
        .attr("x1", function(d) { return d.source.x; })
        .attr("y1", function(d) { return d.source.y; })
        .attr("x2", function(d) { return d.target.x; })
        .attr("y2", function(d) { return d.target.y; });

    node
        .attr("transform", function(d) {
          return "translate(" + d.x + "," + d.y + ")";
        });
  }
});
// print (d.source.x)
// 三つのイベント（start, drag, end）リスナー実装
function dragstarted(d) {
  if (!d3.event.active) simulation.alphaTarget(0.3).restart();
  d.fx = d.x;
  d.fy = d.y;
}

function dragged(d) {
  d.fx = d3.event.x;
  d.fy = d3.event.y;
}

function dragended(d) {
  if (!d3.event.active) simulation.alphaTarget(0);
  d.fx = null;
  d.fy = null;
}

const createLabelElements = (labels) => {
  let label_element = "";
  for (const label of labels) {
    const icon = label.links.length === 0
      ? ``
      : `<i data-toggle="collapse" data-parent="#network_labels" href="#page_${label.id}" class="fas fa-chevron-down icon"></i>`
    label_element = label_element +
    `<div class="panel panel-default" id="title_${label.id}">
      <div class="panel-heading">
        <h3 style="display: flex" class="panel-title">
            ${icon}　<div class="color_label" style="background-color: ${label.color};"></div>${label.id}: ${label.text}
          </a>
        </h3>
      </div>
      ${createLinksElements(label)}
    </div>`
  }
  return label_element;
}

const createLinksElements = (label) => {
  let link_element = "";
  const uniq_links = [...new Map(label.links.map(link => [link.text, link])).values()];
  for (const [i, link] of uniq_links.entries()) {
    const num = label.links.filter(l => l.text === link.text).length;
    link_element = link_element + `<div class="panel-body">${i+1}. ${link.text}<span style="position: absolute; right: 30px">${num}</span></div>`;
  }
  return `<div id="page_${label.id}" class="panel-collapse collapse">${link_element}</div>`;
}

const onClickCircle = (data) => {
  var dialog = document.getElementById("dialog");
    dialog.innerHTML = `<p>id: ${data.id}</p><p>question: ${data.text}</p>`;
    dialog.style.display = 'block';
}

document.getElementById("dialog").onclick = function() {
  this.style.display = 'none';
};