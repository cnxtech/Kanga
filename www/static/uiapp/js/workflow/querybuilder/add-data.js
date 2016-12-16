var GraphLoader = {};

GraphLoader.data = [];
GraphLoader.plot = null;

GraphLoader.init = function () {
    this.resetData();
    this.plot = $.plot("#flot-dashboard-chart", [this.createGraphData(0)],
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
            xaxis: {
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
}

GraphLoader.resetData = function(){
    this.data = [];
    while (this.data.length < 300) {
        this.data.push(0);
    }
}

GraphLoader.pushDataGraph = function (y) {
    this.plot.setData([this.createGraphData(y)]);
    this.plot.draw();
}

GraphLoader.createGraphData = function (y) {
    if (this.data.length > 0)
        this.data = this.data.slice(1);

    // Do a random walk
    //console.log(y);
    this.data.push(y);

    // Zip the generated y values with the x values
    var res = [];
    for (var i = 0; i < this.data.length; ++i) {
        res.push([i, this.data[i]])
    }
    return res;
}



var TopicLoader = {};

TopicLoader.socket = null;

TopicLoader.init = function () {
    this.socket = io.connect("/workspace");
    this.socket.on("cpu_data", function (data) {
        console.log(data)
        GraphLoader.pushDataGraph(parseInt(data.point));
    });
    this.socket.on("disconnect", function () {
        console.log("client disconnected from server");
    });
    this.socket.on("connect", function () {
        console.log("client Connected into server");
        //socket.emit('join', "room_1");
    });
    this.socket.on('error', function (e) {
        console.log('System', e ? e : 'A unknown error occurred');
    });
    this.socket.on('announcement', function (msg) {
        console.log("New Announcement Received")
    });
    this.socket.on('nicknames', function (nicknames) {
        console.log("Nickname received")
    });
    this.socket.on('msg_to_room', function (from, msg) {
        console.log("new message")
    });
}

TopicLoader.reloadTopicList = function () {
    var $el = $("#topic-list");
    $el.empty(); // remove old options
    $.ajax({
        type: 'GET',
        "url": HOST + '{% url 'workspace:kafka-topic-list' %}',
        data: {},
        "beforeSend": function (xhr, settings) {
            $.ajaxSettings.beforeSend(xhr, settings);
        },
        success: function (b) {
            console.log("topic-list loaded:");
            console.log(b)
            $.each(b.data, function (index, row) {
                console.log(row)
                $el.append($("<option></option>").attr("value", row.name).text(row.title));
            });
        },
        error: function (e) {
            console.log(e)
            toastr.warning('Failed to load workflow data', '' + e.responseText);
        }
    });
}




$(document).ready(function () {
    var previousTopic = null;

    $("#stop-workflow").click(function () {
        var $topic = $("#topic-list");
        if ($(this).html() == "stop") {
            $(this).prop("disabled","disabled");
            TopicLoader.socket.emit('user message', {command: "stop"}, function (set) {
               console.log(set);
               var btn = $("#stop-workflow");
               btn.prop("disabled","");
               if(set){
                    btn.html("start");
                    $topic.prop("disabled", "");
               }
            });
        } else if ($(this).html() == "start") {
            var val = $topic.find(":selected").val();
            console.log("start >> "+val);
            if (val != "" && val != null) {
                if(previousTopic != val){
                   GraphLoader.resetData();
                   GraphLoader.pushDataGraph(0);
                }
                previousTopic = val;
                $(this).prop("disabled","disabled");
                console.log("socket emit >>");
                TopicLoader.socket.emit('user message', {command: "start", topic: val}, function (set) {
                    console.log(set);
                    var btn = $("#stop-workflow");
                    btn.prop("disabled","");
                    if(set){
                        $topic.prop("disabled", "disabled");
                        btn.html("stop")
                    }
                });
            } else {
                alert("Select topic first!")
            }
        }
    });

    GraphLoader.init();
    TopicLoader.init();
    TopicLoader.reloadTopicList();
});