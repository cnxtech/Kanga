$(document).ready(function() {
    var data = [],
        totalPoints = 300;

    function initData() {
        while (data.length < totalPoints) {
            data.push(0);
        }
    }
    initData();

    function getRandomData(y) {

        if (data.length > 0)
            data = data.slice(1);

        // Do a random walk
        console.log(y);
        data.push(y);

        // Zip the generated y values with the x values

        var res = [];
        for (var i = 0; i < data.length; ++i) {
            res.push([i, data[i]])
        }

        return res;
    }

    var plot = $.plot("#flot-dashboard-chart", [ getRandomData(50) ],
            {
                series: {
                    lines: {
                        show: true,
                        fill: true
                    },
                    splines: {
                        show: false,
                        tension: 0.4,
                        lineWidth: 1,
                        fill: 0.4
                    },
                    points: {
                        radius: 0,
                        show: true
                    },
                    shadowSize: 2
                },
                grid: {
                    hoverable: true,
                    clickable: true,
                    tickColor: "#d5d5d5",
                    borderWidth: 1,
                    color: '#d5d5d5'
                },
                colors: ["#1ab394"],
                xaxis:{
                    show: false
                },
                yaxis: {
                    ticks: 4,
                    min: 0,
                    max: 100
                },
                tooltip: false
            }
    );

    function update(y) {
        plot.setData([getRandomData(y)]);
        plot.draw();
    }

    update(50);

    function connect() {
        socket = new WebSocket("ws://kanga/ws");

        socket.binaryType = "arraybuffer";

        socket.onopen = function() {
            console.log("Connected to WebSocket server");
            isopen = true;
        }

        socket.onmessage = function(e) {
            update(parseInt(e.data));
        }

        socket.onclose = function(e) {
            console.log("WebSocket connection closed");
        }
    }

    connect();
});
