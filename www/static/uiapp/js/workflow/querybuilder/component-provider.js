/**
 * Created by SRIN on 1/14/2015.
 */
var instance;

function ComponentProvider() {
    this.currentNodes = [];
    this.queryParentID = ".query-list";
    this.canvasID = "#flowchart-canvas";
    this.queryDisplayerID = "#portlet_tab_2";
    this.numberOfElements = 0;
    this.componentImagePath = "/static/uiapp/img/components/";
    this.componentType = {
        HIVE: "hive",
        HADOOP: "hadoop",
        PIG: "pig",
        MYSQL: "mysql",
        LOG: "log"
    }
// this is the paint style for the connecting lines..
    this.connectorPaintStyle = {
        lineWidth: 4,
        strokeStyle: "#61B7CF",
        joinstyle: "round",
        outlineColor: "white",
        outlineWidth: 2
    }

    // .. and this is the hover style.
    this.connectorHoverStyle = {
        lineWidth: 4,
        strokeStyle: "#216477",
        outlineWidth: 2,
        outlineColor: "white"
    }
    this.endpointHoverStyle = {
        fillStyle: "#216477",
        strokeStyle: "#216477"
    }
// the definition of source endpoints (the small blue ones)
    this.sourceEndpoint = {
        endpoint: "Dot",
        paintStyle: {
            strokeStyle: "#1ab394",
            fillStyle: "transparent",
            radius: 7,
            lineWidth: 3
        },
        maxConnections: -1,
        isSource: true,
        connector: ["Flowchart", {stub: [40, 60], gap: 10, cornerRadius: 5, alwaysRespectStubs: true}],
        connectorStyle: this.connectorPaintStyle,
        hoverPaintStyle: this.endpointHoverStyle,
        connectorHoverStyle: this.connectorHoverStyle,
        dragOptions: {},
        overlays: [
            ["Label", {
                location: [0.5, 1.5],
                label: "Output",
                cssClass: "endpointSourceLabel"
            }]
        ]
    }
// the definition of target endpoints (will appear when the user drags a connection)
    this.targetEndpoint = {
        endpoint: "Dot",
        paintStyle: {
            strokeStyle: "#1cc09f",
            fillStyle: "#1cc09f",
            radius: 7,
            lineWidth: 3
        },
        hoverPaintStyle: this.endpointHoverStyle,
        maxConnections: -1,
        dropOptions: {hoverClass: "hover", activeClass: "active"},
        isTarget: true,
        overlays: [
            ["Label", {location: [0.5, -0.5], label: "Input", cssClass: "endpointTargetLabel"}]
        ]
    }

    this.init = function (connection) {
        connection.getOverlay("label").setLabel(connection.sourceId.substring(15) + "-" + connection.targetId.substring(15));
        connection.bind("editCompleted", function (o) {
            if (typeof console != "undefined")
                console.log("connection edited. path is now ", o.path);
        });
    };

    this._addEndpoints = function (toId, sourceAnchors, targetAnchors) {
        var tmpEP1 = []
        var tmpEP2 = []

        for (var i = 0; i < sourceAnchors.length; i++) {
            var sourceUUID = toId + sourceAnchors[i];
            console.log(sourceUUID+"<<<<<<<<<<<<")

            var ep = instance.addEndpoint(toId, this.sourceEndpoint, {anchor: sourceAnchors[i], uuid: sourceUUID});
            tmpEP1.push(ep);
        }
        for (var j = 0; j < targetAnchors.length; j++) {
            var targetUUID = toId + targetAnchors[j];
            var ep = instance.addEndpoint(toId, this.targetEndpoint, {anchor: targetAnchors[j], uuid: targetUUID});
            tmpEP2.push(ep);
        }

        this.currentNodes.push({
            nodeID: toId,
            epSources: tmpEP1,
            epOutputs: tmpEP2
        });
        //console.log("CURRENTNODE LEN: "+this.currentNodes.length);
    };

    /**
     * ADD NEW COMPONENT WITH AUTO NAMING
     * @param type
     * @param topPos
     * @param leftPos
     */
    this.addNewComponent = function(type, topPos, leftPos, icon) {
        var obj = new Date();
        var ms = "flowchart_"+type+"_"+obj.getMilliseconds();
        this.addComponent(ms, type, topPos, leftPos, icon);
    }
    this.addComponent = function(componentID, type, topPos, leftPos, icon) {
        this.addComponent(componentID, type, topPos, leftPos, icon, null);
    }    /*
     * ADD COMPONENT INTO CANVAS WITHOUT AUTO NAMING
     */
    this.addComponent = function(componentID, type, topPos, leftPos, icon, argData) {
        console.log("Component ID:"+componentID+" | type: "+type);
        //var imageSrc = this.componentImagePath+icon;

        var Div = $('<div>', {id:componentID}, {class: 'window'}).css({
            border: 'solid 1px',
            top: topPos+'px',
            left: leftPos+'px'
        }).appendTo(this.canvasID);

        $(Div).attr('data-nodetype',type);
        if(argData != null)
            $(Div).attr('arg-data',argData);
        Div.html('' +
        '<i class="fa fa-close window-remover" parentid="'+componentID+'" id="window-remover-01"></i>' +
        '<span class="processor-snippet">'+icon+'</span>');
        $(Div).addClass('window');
        this._addEndpoints(componentID, ["BottomCenter"], ["TopCenter"]);
        instance.draggable(jsPlumb.getSelector(".flowchart-canvas .window"), { grid: [20, 20] });

    }

    this.getFlowchartHeight = function(){
        var tallest = -1;
        $(".window").each(function (idx, elem){
            var $elem = $(elem)
            //var endpoints = jsPlumb.getEndpoints($elem.attr('id'));
            var tmp = parseInt($elem.css('top'), 10);
            var tmpH = parseInt($elem.css('height'), 10);
            if(tmp > tallest){
                tallest = tmp + tmpH*2;
            }
        });
        return tallest;
    }

    /**
     * CONVERT DESIGNED QUERY INTO JSON FORMAT
     */
    this.saveFlowchart = function(queryID, queryName, queryDescription, docControllerCallback){
        var nodes = [];
        var numberOfElements
        $(".window").each(function (idx, elem){
            var $elem = $(elem)
            var endpoints = jsPlumb.getEndpoints($elem.attr('id'));
            console.log('endpoints of '+$elem.attr('id'));
            console.log(endpoints);
            nodes.push({
                blockId: $elem.attr('id'),
                nodetype: $elem.attr('data-nodetype'),
                positionX: parseInt($elem.css('left'), 10),
                positionY: parseInt($elem.css('top'), 10),
                argData: $elem.attr('arg-data'),
                snippet: $elem.find("span").html()
            });
        });

        var connections = [];
        console.log(instance.getConnections());
        $.each(instance.getConnections(), function(idx, connection){
            console.log(connection);
            connections.push({
                connectionId: connection.uuids,
                pageSourceId: connection.sourceId,
                pageTargetId: connection.targetId
            });
        });

        var flowchart = {};
        //flowchart.id = queryID;
        //flowchart.name = queryName;
        flowchart.nodes = nodes;
        flowchart.connections = connections;
        flowchart.numberOfElements = numberOfElements;

        var flowChartJson = JSON.stringify(flowchart);
        console.log(flowChartJson);
        console.log(queryID);

        // SAVE TO DOM
        var Div = $('<li>').attr('onclick',"c.loadFlowchart('"+flowChartJson+"')").html("<a href='#'>"+queryName+"</a>").appendTo(this.queryParentID);

        // SAVE TO BACKEND
        $.ajax({
            type: 'POST',
            url: HOST + '/workspace/querybuilder/save/',
            data: {
                id: queryID,
                name: queryName,
                description: queryDescription,
                data: flowChartJson
            },
            "beforeSend": function(xhr, settings) {
                console.log("Before Send");
                $.ajaxSettings.beforeSend(xhr, settings);
            },
            success: function (b) {
                if (b && b.id != null) {
                    docControllerCallback.flagAsEditDocument(b.id);
                    $("#save-workflow").html("Save");
                    toastr.success('Workflow "'+queryName+'" saved successfully!', '');
                }else{
                    toastr.warning('Failed to save workflow', 'Invalid response from server.');
                }
            },
            error: function (e) {
                console.log(e)
                toastr.warning('Failed to save workflow, please try again later', '' );//+ e.responseText);
            }
        });
    }

    /**
     * CONVERT JSON DATA INTO QUERY DESIGNER FORM
     *
     * * @param flowchartJson
     */
    this.drawWorkflow = function(wfid, wfname, wfdescription, flowchartJson, docControllerCallback){
        var flowchart = JSON.parse(flowchartJson);
        var nodes = flowchart.nodes;
        //var queryName = flowchart.name;
        var mInstance = this;

        $("#builder-query-name").html(""+wfname);
        $("#builder-query-description").html(""+wfdescription);

        $.each(nodes, function(index, node){
            console.log(this);
            mInstance.addComponent(node.blockId, node.nodetype, node.positionY, node.positionX, node.snippet, node.argData);
        });

        var connections = flowchart.connections;
        $.each(connections, function( index, elem ) {
            console.log("SourceID: "+elem.pageSourceId);
            console.log("TargetID: "+elem.pageTargetId);
            instance.connect({uuids:[elem.pageSourceId+"BottomCenter", elem.pageTargetId+"TopCenter"], editable:true});
        });

        docControllerCallback.flagAsEditDocument(wfid, wfname);
    }

    this.loadWorkflow = function(queryID, docControllerCallback){
        console.log("WFID : "+queryID)
        var parent = this;
        $.ajax({
            type: 'POST',
            url: HOST + '/workspace/batch-query/detail/',
            data: {
                id: queryID
            },
            "beforeSend": function(xhr, settings) {
                $.ajaxSettings.beforeSend(xhr, settings);
            },
            success: function (b) {
                console.log("Workflow data loaded");
                if (b && b.status == null) {
                    console.log(b);
                    parent.drawWorkflow(b.id, b.name, b.description, b.data, docControllerCallback);
                    $("#save-workflow").html("Save");
                    docControllerCallback.resizeFitCanvas(parent.getFlowchartHeight())
                }else if(b.message != null){
                    toastr.warning(b.message, '');
                }
            },
            error: function (e) {
                console.log(e)
                toastr.warning('Failed to load workflow data', '' + e.responseText);
            }
        });
    }

    this.clearNodesData = function(){
        this.currentNodes = [];
    }
}


jsPlumb.ready(function () {

    instance = jsPlumb.getInstance({
        // default drag options
        DragOptions: {cursor: 'pointer', zIndex: 2000},
        // the overlays to decorate each connection with.  note that the label overlay uses a function to generate the label text; in this
        // case it returns the 'labelText' member that we set on each connection in the 'init' method below.
        /*ConnectionOverlays: [
            ["Arrow", {location: 1}],
            ["Label", {
                location: 0.1,
                id: "label",
                cssClass: "aLabel"
            }]
        ],*/
        Container: "flowchart-canvas"
    });


    // suspend drawing and initialise.
    instance.doWhileSuspended(function () {
        /*
         c = new componentProvide();
         //_addEndpoints("Window4", ["TopCenter", "BottomCenter"], ["LeftMiddle", "RightMiddle"]);
         //_addEndpoints("Window2", ["LeftMiddle", "BottomCenter"], ["TopCenter", "RightMiddle"]);
         //c._addEndpoints("Window3", ["RightMiddle", "BottomCenter"], ["LeftMiddle", "TopCenter"]);
         c._addEndpoints("Window1", ["LeftMiddle", "RightMiddle"], ["TopCenter", "BottomCenter"]);
         // listen for new connections; initialise them the same way we initialise the connections at startup.
         instance.bind("connection", function(connInfo, originalEvent) {
         c.init(connInfo.connection);
         });*/

        // make all the window divs draggable
        //instance.draggable(jsPlumb.getSelector(".flowchart-canvas .window"), { grid: [20, 20] });
        // THIS DEMO ONLY USES getSelector FOR CONVENIENCE. Use your library's appropriate selector
        // method, or document.querySelectorAll:
        //jsPlumb.draggable(document.querySelectorAll(".window"), { grid: [20, 20] });

        // connect a few up
        //instance.connect({uuids:["Window2BottomCenter", "Window3TopCenter"], editable:true});
        //instance.connect({uuids:["Window2LeftMiddle", "Window4LeftMiddle"], editable:true});
        //instance.connect({uuids:["Window4TopCenter", "Window4RightMiddle"], editable:true});
        //instance.connect({uuids:["Window3RightMiddle", "Window2RightMiddle"], editable:true});
        //instance.connect({uuids:["Window4BottomCenter", "Window1TopCenter"], editable:true});
        //instance.connect({uuids:["Window3BottomCenter", "Window1BottomCenter"], editable:true});
        //

        //
        // listen for clicks on connections, and offer to delete connections on click.
        //
        instance.bind("click", function(conn, originalEvent) {
            if (confirm("Delete connection from " + conn.sourceId + " to " + conn.targetId + "?"))
                jsPlumb.detach(conn);
        });

        instance.bind("connectionDrag", function(connection) {
            console.log("connection " + connection.id + " is being dragged. suspendedElement is ", connection.suspendedElement, " of type ", connection.suspendedElementType);
        });

        instance.bind("connectionDragStop", function(connection) {
            console.log("connection " + connection.id + " was dragged");
        });

        instance.bind("connectionMoved", function(params) {
            console.log("connection " + params.connection.id + " was moved");
        });
    });

    jsPlumb.fire("jsPlumbDemoLoaded", instance);

});

var c = new ComponentProvider();
$(document).ready(function(){
    // Component Toolbox
    $.get(COMPONENT_TOOLBOX_TPL_PATH, function (data) {
        $('body').append(data);
        //$(".toolbox-component").css('background-color','red');
        //Make element draggable from Toolbox into canvas
    });

    //Handle position when dropping component into canvas
    $("#flowchart-canvas").droppable({
        drop: function (ev, ui) {
            try {
                var draggedId = ui.draggable.attr("id");
                var icon = ui.draggable.attr("icon");

                var seg = draggedId.split("-");
                if (seg.length != 0 && seg[0] == ("component")) {
                    var $newPosX = ui.offset.left - $(this).offset().left+$(this).scrollLeft();
                    var $newPosY = ui.offset.top - $(this).offset().top+$(this).scrollTop();
                    c.addNewComponent(seg[1], $newPosY, $newPosX, icon);
                }
            }catch(err){
                console.log(err.message);
            }
        }
    });


    // SAVE & LOAD DESIGNED QUERY
    $("#save-query").click(function(){
        c.saveFlowchart();
    });

});
