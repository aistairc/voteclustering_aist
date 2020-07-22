//------------------- SankeyDiagram表示 ------------------
var layout = d3.sankey()
        .nodeWidth(15)
        .extent([[120, 10], [980, 680]]);

var color = d3.scaleOrdinal(d3.schemeCategory10);
var diagram = d3.sankeyDiagram()
  .nodeTitle(function(node) { // ノードのタイトルを略記
    node.title = node.title.replace("question", "q");
    node.title = node.title.replace("option", "o");
    return node.title;
  })
  .linkColor(function(d){return color(d.type);});

var el = d3.select('#sankey svg')
    .datum(layout(data))
    .call(diagram);   // (c)

//--------------------- SVGをPNG/JPG/PDF形式で保存 -----------------------

var svg = d3.select('svg');
var width = d3.select('svg').attr('width', SVG_WIDTH);
var height = d3.select('svg').attr('height');
// Set-up the export button
d3.select('#saveButton').on('click', function(){
  var extention = document.getElementById('extention').value; // 選択された拡張子を取得
    var svgString = getSVGString(svg.node());

    svgString2Image( svgString, 2*width, 2*height, extention, save ); // passes Blob and filesize String to the callback

    function save(dataBlob, filesize, extention){
    if(extention == "pdf") { // PDF保存
      var url = window.URL || window.webkitURL;
      var pdf = new jsPDF('p', 'px', [2*width, 2*height]);
      var imgSrc = url.createObjectURL(dataBlob);
      var img = new Image();
      img.src = imgSrc;
      img.onload = function () {
        pdf.addImage(img, 0, 0, width, height);
        pdf.save('d3_sankey_diagram.pdf');
      };
    } else { // PDF以外保存
      saveAs( dataBlob, 'd3_sankey_diagram.' + extention ); // FileSaver.js function
    }
    }


});

// Below are the functions that handle actual exporting:
// getSVGString ( svgNode ) and svgString2Image( svgString, width, height, format, callback )
function getSVGString( svgNode ) {
    svgNode.setAttribute('xlink', 'http://www.w3.org/1999/xlink');
    var cssStyleText = getCSSStyles( svgNode );
    appendCSS( cssStyleText, svgNode );

    var serializer = new XMLSerializer();
    var svgString = serializer.serializeToString(svgNode);
    svgString = svgString.replace(/(\w+)?:?xlink=/g, 'xmlns:xlink='); // Fix root xlink without namespace
    svgString = svgString.replace(/NS\d+:href/g, 'xlink:href'); // Safari NS namespace fix

    return svgString;

    function getCSSStyles( parentElement ) {
        var selectorTextArr = [];

        // Add Parent element Id and Classes to the list
        selectorTextArr.push( '#'+parentElement.id );
        for (var c = 0; c < parentElement.classList.length; c++)
                if ( !contains('.'+parentElement.classList[c], selectorTextArr) )
                    selectorTextArr.push( '.'+parentElement.classList[c] );

        // Add Children element Ids and Classes to the list
        var nodes = parentElement.getElementsByTagName("*");
        for (var i = 0; i < nodes.length; i++) {
            var id = nodes[i].id;
            if ( !contains('#'+id, selectorTextArr) )
                selectorTextArr.push( '#'+id );

            var classes = nodes[i].classList;
            for (var c = 0; c < classes.length; c++)
                if ( !contains('.'+classes[c], selectorTextArr) )
                    selectorTextArr.push( '.'+classes[c] );
        }

        // Extract CSS Rules
        var extractedCSSText = "";
        for (var i = 0; i < document.styleSheets.length; i++) {
            var s = document.styleSheets[i];

            try {
                if(!s.cssRules) continue;
            } catch( e ) {
                    if(e.name !== 'SecurityError') throw e; // for Firefox
                    continue;
                }

            var cssRules = s.cssRules;
            for (var r = 0; r < cssRules.length; r++) {
                if ( contains( cssRules[r].selectorText, selectorTextArr ) )
                    extractedCSSText += cssRules[r].cssText;
            }
        }


        return extractedCSSText;

        function contains(str,arr) {
            return arr.indexOf( str ) === -1 ? false : true;
        }

    }

    function appendCSS( cssText, element ) {
        var styleElement = document.createElement("style");
        styleElement.setAttribute("type","text/css");
        styleElement.innerHTML = cssText;
        var refNode = element.hasChildNodes() ? element.children[0] : null;
        element.insertBefore( styleElement, refNode );
    }
}


function svgString2Image( svgString, width, height, format, callback ) {
    var format = format ? format : 'png';

  // Blobに変換する際に指定が必要MIMEタイプを設定
  var mimeType = ""
  switch(format){
    case "png":
      mimeType = "image/png";
      break;
    case "jpg":
      mimeType = "image/jpeg";
      break;
    case "pdf":
      mimeType = "application/pdf";
      break;
    default:
      mimeType = "image/png";
      break;
  }

    var imgsrc = 'data:image/svg+xml;base64,'+ btoa( unescape( encodeURIComponent( svgString ) ) ); // Convert SVG string to data URL

    var canvas = document.createElement("canvas");
    var context = canvas.getContext("2d");

    canvas.width = width;
    canvas.height = height;

    var image = new Image();
    image.onload = function() {
        context.clearRect ( 0, 0, width, height );
        context.drawImage(image, 0, 0, width, height);

        canvas.toBlob( function(blob) {
            var filesize = Math.round( blob.length/1024 ) + ' KB';
            if ( callback ) callback( blob, filesize, format );
        }, mimeType);
    };

    image.src = imgsrc;
}
