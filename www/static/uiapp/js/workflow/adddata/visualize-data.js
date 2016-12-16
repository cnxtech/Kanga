var socket = false;
var dtRowCount = 0;
var dtFields = [];
var dtColumns = [];
var data = [];
var dt;
var Row;
var dtrows = ko.mapping.fromJS( [] );
var isopen = false;

function disconnect(){
    console.log('request connection close');
    if (socket) socket.close();
    socket = false;
    dtRowCount = 0;
}

function connect() {
    if (isopen==true) disconnect();
//    socket = new WebSocket("ws://kanga/ws");
    socket = new WebSocket("ws://10.251.21.176/ws");
    socket.binaryType = "arraybuffer";

    socket.onopen = function() {
        console.log("Connected to WebSocket server");
        isopen = true;
    }

    socket.onmessage = function(e) {
        //update(parseInt(e.data));
        var json = JSON.parse(e.data);
        data.push(json.data[0]);
//        console.log(json.data[0]);
        if ( dtRowCount == 0 ) {
            dtFields = Object.keys(json.data[0]);
            var mycolumns = [];
            var dtHtml = '<thead><tr>';
            var initdata = {};
            var ctFields = dtFields.length;
            var tmp;
            for (i=0;i<ctFields;i++){
                dtHtml = dtHtml +  '<th>' + dtFields[i] + '</th>';
                mycolumns.push({data:dtFields[i]});
                console.log(json.data[0][dtFields[i]]);
                initdata[dtFields[i]] = json.data[0][dtFields[i]];
                tmp = tmp + dtFields[i] +",";
            }
            console.log(initdata);
            console.log(tmp);
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
                    [ 10, "desc" ]
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
//        console.log(Object.keys(json.data[0]).length);
    }

    socket.onclose = function(e) {
        console.log("WebSocket connection closed");
        dtRowCount = 0;
        isopen = false;
    }
}
$(document).ready(function() {


    dtrows.subscribeArrayChanged(
        function ( addedItem ) {
            dt.row.add( addedItem ).draw();
        }
    );



});