/**
 * Created by chelalimohamed-tayeb on 08/05/2017.
 */
function creatGraph(id) {

    var width = 960,
        height = 500

    var svg = d3.select("#graph").append("svg")
        .attr("width", width)
        .attr("height", height);

    var force = d3.layout.force()
        .gravity(.05)
        .distance(100)
        .charge(-100)
        .size([width, height]);

    d3.json("/graphI/"+id, function (json) {
        force
            .nodes(json.nodes)
            .links(json.links)
            .start();

        var link = svg.selectAll(".link")
            .data(json.links)
            .enter().append("line")
            .attr("class", "link")
            .style("stroke-width", function (d) {
                return Math.sqrt(d.weight);
            });

        var node = svg.selectAll(".node")
            .data(json.nodes)
            .enter().append("g")
            .attr("class", "node")
            .call(force.drag);

        node.append("circle")
            .attr("r", "5");

        node.append("text")
            .attr("dx", 12)
            .attr("dy", ".35em")
            .text(function (d) {
                return d.name
            });
        link.append("text")
            .attr("dx", 12)
            .attr("dy", ".35em")
            .text(function (d) {
                return d.name
            });

        force.on("tick", function () {
            link.attr("x1", function (d) {
                return d.source.x;
            })
                .attr("y1", function (d) {
                    return d.source.y;
                })
                .attr("x2", function (d) {
                    return d.target.x;
                })
                .attr("y2", function (d) {
                    return d.target.y;
                });

            node.attr("transform", function (d) {
                return "translate(" + d.x + "," + d.y + ")";
            });
        });

         svg.selectAll(".node").on("click", function (d) {
             console.log(d)
            var info = {}
            $.get("/getNodeInfo/"+d.id, function(data){
                console.log(data);
                info = data;
                window.loadInformation(info);
            });
         })


    });
}

function createGraph2(id) {
    var w = 1000;
    var h = 600;
    var linkDistance=200;

    var colors = d3.scale.category10();


    var svg = d3.select("#graph").append("svg").attr({"width":w,"height":h});

    d3.json("/graphI/"+id, function (dataset){

        var force = d3.layout.force()
        .nodes(dataset.nodes)
        .links(dataset.links)
        .size([w,h])
        .linkDistance([linkDistance])
        .charge([-500])
        .theta(0.1)
        .gravity(0.05)
        .start();



        var edges = svg.selectAll("line")
          .data(dataset.links)
          .enter()
          .append("line")
          .attr("id",function(d,i) {return 'edge'+i})
          .attr('marker-end','url(#arrowhead)')
          .style("stroke","#f009")
          .style("pointer-events", "none");

        var nodes = svg.selectAll("circle")
          .data(dataset.nodes)
          .enter()
          .append("circle")
          .attr({"r":15})
          .style("fill",function(d,i){return colors(i);})
          .call(force.drag)


        var nodelabels = svg.selectAll(".nodelabel")
           .data(dataset.nodes)
           .enter()
           .append("text")
           .attr({"x":function(d){return d.x;},
                  "y":function(d){return d.y;},
                  "class":"nodelabel",
                  "stroke":"#0000"})
           .text(function(d){return d.name;});

        var edgepaths = svg.selectAll(".edgepath")
            .data(dataset.links)
            .enter()
            .append('path')
            .attr({'d': function(d) {return 'M '+d.source.x+' '+d.source.y+' L '+ d.target.x +' '+d.target.y},
                   'class':'edgepath',
                   'fill-opacity':0,
                   'stroke-opacity':0,
                   'fill':'blue',
                   'stroke':'red',
                   'id':function(d,i) {return 'edgepath'+i}})
            .style("pointer-events", "none");

        var edgelabels = svg.selectAll(".edgelabel")
            .data(dataset.links)
            .enter()
            .append('text')
            .style("pointer-events", "none")
            .attr({'class':'edgelabel',
                   'id':function(d,i){return 'edgelabel'+i},
                   'dx':80,
                   'dy':0,
                   'font-size':10,
                   'fill':'#aaa'});

        edgelabels.append('textPath')
            .attr('xlink:href',function(d,i) {return '#edgepath'+i})
            .style("pointer-events", "none")
            .text(function(d,i){return d.name});


        svg.append('defs').append('marker')
            .attr({'id':'arrowhead',
                   'viewBox':'-0 -5 10 10',
                   'refX':25,
                   'refY':0,
                   //'markerUnits':'strokeWidth',
                   'orient':'auto',
                   'markerWidth':10,
                   'markerHeight':10,
                   'xoverflow':'visible'})
            .append('svg:path')
                .attr('d', 'M 0,-5 L 10 ,0 L 0,5')
                .attr('fill', '#ccc')
                .attr('stroke','#ccc');


        force.on("tick", function(){

            edges.attr({"x1": function(d){return d.source.x;},
                        "y1": function(d){return d.source.y;},
                        "x2": function(d){return d.target.x;},
                        "y2": function(d){return d.target.y;}
            });

            nodes.attr({"cx":function(d){return d.x;},
                        "cy":function(d){return d.y;}
            });

            nodelabels.attr("x", function(d) { return d.x; })
                      .attr("y", function(d) { return d.y; });

            edgepaths.attr('d', function(d) { var path='M '+d.source.x+' '+d.source.y+' L '+ d.target.x +' '+d.target.y;
                                               //console.log(d)
                                               return path});

            edgelabels.attr('transform',function(d,i){
                if (d.target.x<d.source.x){
                    bbox = this.getBBox();
                    rx = bbox.x+bbox.width/2;
                    ry = bbox.y+bbox.height/2;
                    return 'rotate(180 '+rx+' '+ry+')';
                    }
                else {
                    return 'rotate(0)';
                    }
            });
        });

        svg.selectAll("circle").on("click", function (d) {
             console.log(d)
            var info = {}
            $.get("/getNodeInfo/"+d.id, function(data){
                console.log(data);
                info = data;
                window.loadInformation(info);
            });
         })

    });
}



