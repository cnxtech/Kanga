var socket = false;
var dtRowCount = 0;
var dtFields = [];
var dtColumns = [];
var data = [];
var dt;
var Row;
var dtrows = ko.mapping.fromJS( [] );
var isopen = false;
var topic_name = "cnc_log_topic";



var TopicSubscriber = {};
TopicSubscriber.socket = null;
TopicSubscriber.init = function () {
    this.socket = io.connect("/workspace");
    console.log(this.socket);
    this.socket.on("ws"+topic_name, function (msg) {
//        console.log(msg);
        update_dataTables(msg);
        alert_toastr(msg);
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


function cnc_data_subscribe() {
    TopicSubscriber.init();
    console.log("start >> ");
    TopicSubscriber.socket.emit('user message', {command: "start", topic: topic_name, pid: topic_name}, function (set) {
        console.log(set);
    });
}

function alert_toastr(msg) {
    var json = JSON.parse(msg);
    if(json.data[0]["DEFECT"]!="PASS") {
        alert_msg = json.data[0]["Equipment_ID"] + " @"+ json.data[0]["ARRIVAL_TIMESTAMP"];
        toastr.options = {
            "timeOut": "1000",
        }
        toastr.error(alert_msg);
    }
}


function update_dataTables(msg) {
    var json = JSON.parse(msg);
//    console.log(json.data[0]);
    data.push(json.data[0]);
    if ( dtRowCount == 0 ) {
        dtFields = Object.keys(json.data[0]);
        var mycolumns = [];
        var dtHtml = '<thead><tr>';
        var initdata = {};
        var ctFields = dtFields.length;
        for (i=0;i<ctFields;i++){
            dtHtml = dtHtml +  '<th>' + dtFields[i] + '</th>';
            mycolumns.push({data:dtFields[i]});
            console.log(json.data[0][dtFields[i]]);
            initdata[dtFields[i]] = json.data[0][dtFields[i]];
        }
//        console.log(initdata);
        dtHtml = dtHtml +  '</tr></thead><tbody></tbody>';
        $("#dataTables-query-result").html(dtHtml);
        $("#dataTables-query-result").css({
            "padding": "0",
            "border-spacing": "0",
            "border": "0",
            "width": "100%",
        }).addClass('table').addClass('table-hover');
        dt = $("#dataTables-query-result").DataTable({
            columns: mycolumns,
            order: [
                [ 0, "desc" ]
            ],
            bDestroy: true,
            language: {"search": "Search: "},
        });
        dt.row.add(initdata).draw();
        dtRowCount++;
        Row = function(row, dt) {
            for(i=0;i<ctFields;i++){
                eval("this."+dtFields[i]+" = ko.observable(row."+dtFields[i]+")");
            }
        };
    }else{
        dtrows.push(new Row(json.data[0],dt));
    }
    if ( json.data[0]['DEFECT'].indexOf("FAIL") > -1  ){
        total_cnc_failure = total_cnc_failure + 1;
    } else {
        total_cnc_success = total_cnc_success + 1;
    }
    statsViewModel.totalNumOfSET(numberWithCommas(getTotalSet()));
    statsViewModel.totalCNCTestSuccess(numberWithCommas(total_cnc_success));
    statsViewModel.totalCNCTestFailure(numberWithCommas(total_cnc_failure));
    statsViewModel.totalDefect(numberWithCommas(getTotalDefect()));
//        console.log(Object.keys(json.data[0]).length);
}




$(document).ready(function() {


    dtrows.subscribeArrayChanged(
        function ( addedItem ) {
            dt.row.add( addedItem ).draw();
        }
    );
    cnc_data_subscribe();



});