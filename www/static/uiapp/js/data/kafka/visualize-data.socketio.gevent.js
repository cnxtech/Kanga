var max_table_rows = 100;
var samples = [];
var samplesGridOptions = {
    dataSource: samples,
    loadPanel: false,
    allowColumnReordering: true,
    allowColumnResizing: true,
    columnAutoWidth: true,
    rowAlternationEnabled: true,
    showRowLines: true,
    noDataText: "No incoming event from the selected Kafka queue.",
    groupPanel: {
        visible: true
    },
    export: {
        enabled: true,
        fileName: "DataGrid",
        allowExportSelectedData: false
    },
    columnChooser: {
        enabled: true,
        height: 180,
        width: 400,
        emptyPanelText: 'A place to hide the columns'
    },
//        filterRow: {
//            visible: true,
//            applyFilter: "auto"
//        },
    headerFilter: {
        visible: true
    },
    searchPanel: {
        visible: true,
        width: 240,
        placeholder: 'Search...'
    },
    sorting: {
        mode: 'multiple'
    },
    paging: {
        pageSize: 10
    },
    pager: {
        showPageSizeSelector: true,
        allowedPageSizes: [5, 10, 20]
    }
};
var datatable_topic_sample = $("#datatable-topic-sample").dxDataGrid(samplesGridOptions).dxDataGrid("instance");












var TopicSubscriber = {};
TopicSubscriber.socket = null;
TopicSubscriber.init = function () {
    this.socket = io.connect("/data");
    console.log(this.socket);
    this.socket.on(topic_name, function (msg) {
//        console.log(msg);
        update_data(msg);
//        alert_toastr(msg)
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


function topic_subscribe() {
    TopicSubscriber.init();
    console.log("start >> ");
    TopicSubscriber.socket.emit('user message', {command: "start", topic: topic_name, pid: topic_name}, function (set) {
        console.log(set);
        subscribing = true;
    });
}







function update_data(msg) {
    msg = msg.replace(/[\x00-\x1F\x7F-\x9F]/g, "");   // remove all non-printable characters
    var json = JSON.parse(msg);
    samples.push({"arrival_time":timeConverterLong(Date.now()),"message":msg});
    if (samples.length>max_table_rows){
        samples.shift();
    }
    datatable_topic_sample.option({dataSource: samples});
//    console.log(json);
    // raw data

}


var subscribing = false;
$(document).ready(function() {
    topic_subscribe();
    $("#play_button").click(function(){
        console.log("clicked");
        if (subscribing==false){
            TopicSubscriber.socket.emit('user message', {command: "start", topic: topic_name, pid: topic_name}, function (set) {
                console.log(set);
                subscribing = true;
                $("#play_button").html('<i class="fa fa-pause"></i> Pause');
            });
        } else {
            TopicSubscriber.socket.emit('user message', {command: "stop", topic: topic_name, pid: topic_name}, function (set) {
                console.log(set);
                subscribing = false;
                $("#play_button").html('<i class="fa fa-play"></i> Play');
            });
        }
    });
});