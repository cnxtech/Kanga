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












var wSocket;
function init() {
    var url = "ws://"+HOST+":7080/v2/broker/?group.id="+group_id+"&sleeping="+sleeping+"&topics=" + topic_name;
    console.log("init " + url);

    wSocket = new WebSocket(url);
    wSocket.onopen = function (e) { onOpen(e) };
    wSocket.onclose = function (e) { onClose(e) };
    wSocket.onmessage = function (e) { onMessage(e) };
    wSocket.onerror = function (e) { onError(e) };
}
function onOpen(e) {
    console.log(e);
    subscribing = true;
    $("#play_button").html('<i class="fa fa-pause"></i> Pause');
}
function onClose(e) {
    console.log(e);
    subscribing = false;
    $("#play_button").html('<i class="fa fa-play"></i> Play');
}
function onMessage(e) {
    var msg = JSON.parse(e.data);
    update_data(msg.message);
}
function onError(e) {
    console.log("onError " + e.data);
}
function doOpen() {
    init();
}
function doClose() {
    wSocket.close();
}

function update_data(msg) {
    msg = msg.replace(/[\x00-\x1F\x7F-\x9F]/g, "");   // remove all non-printable characters
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
    init();
    $("#play_button").click(function(){
        console.log("clicked");
        if (subscribing==false){
            init();
            $("#play_button").html('<i class="fa fa-spinner fa-spin"></i> Playing');
        } else {
            doClose();
            $("#play_button").html('<i class="fa fa-spinner fa-spin"></i> Pausing');
        }
    });
});