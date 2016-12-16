/**
 * Created by SRIN on 1/14/2015.
 */
var instance;
var ask_validate = false;
var ask_compile = false;
var ask_launch = false;
var dummy_input = false;
var dummy_output = false;
function ComponentProvider() {

    this.nodemap = [
        {
            types: [
                    'sum',
                    'count',
                    'average',
                    'max',
                    'min',
                    'calculate',
                    'stdev',
                ],
            category:"aggregate",
            class:"aggregationnode",
            output:true,
            input:true,
        },
        {
            types: [
                    'sum',
                    'count',
                    'average',
                    'max',
                    'min',
                    'calculate',
                    'stdev',
                ],
            category:"collection",
            class:"aggregationnode",
            output:true,
            input:true,
        },
        {
            types: [
                    'table_filter',
                    'where_clause',
                ],
            category:"filter",
            class:"filternode",
            output:true,
            input:true,
        },
        {
            types: [
                    'passthrough_from_file',
                    'from_kafka',
                    'passthrough_from_database',
                    'passthrough_from_ElasticSearch',
                    'passthrough_from_kafka',
                    'example_generator',
                    'passthrough_from_csvfile',
                    'event_generator',
                ],
            category:"input_stream",
            class:"inputnode",
            output:true,
            input:false,
        },
        {
            types: [
                    'join',
                    'join_by_time',
                    'merge',
                    'sort',
                    'state_join',
                ],
            category:"join",
            class:"joinmergenode",
            output:true,
            input:true,
        },
        {
            types: [
                    'save_to_file',
                    'to_file',
                    'send_email',
                    'insert_into_database',
                    'save_to_kafka',
                    'save_to_elasticsearch',
                ],
            category:"output_stream",
            class:"outputnode",
            output:false,
            input:true,
        },
        {
            types: [
                    'random_tick',
                    'last_tick',
                    'first_tick',
                ],
            category:"sample",
            class:"samplingnode",
            output:true,
            input:true,
        },
        {
            types: [
                    'reformat',
                ],
            category:"oneM2M",
            class:"samplingnode",
            output:true,
            input:true,
        },
        {
            types: [
                    'add_field',
                    'split',
                    'script',
                    'rename_field',
                    'regex',
                    'udpate_field',
                    'remove_fields',
                    'grok_bolt',
                ],
            category:"transform",
            class:"transformationnode",
            output:true,
            input:true,
        },
        {
            types: [
                    'cnc_tool_failure',
                    'cnc_testfile',
                    'philips_hue',
                ],
            category:"third_party",
            class:"thirdpartynode",
            output:true,
            input:true,
        },
        {
            types: [
                    'transaction',
                    'jitter_join',
                ],
            category:"function",
            class:"functionnode",
            output:true,
            input:true,
        },
        {
            types: [
                    'cnc_tool_failure',
                    'cnc_testfile',
                    'philips_hue',
                ],
            category:"na",
            class:"defaultnode",
            output:true,
            input:true,
        },
        {
            types:['dummy_input','dummy_output','dummy_macro'],
            category:"macro",
            class:"functionnode",
            output:false,
            input:false,
        },
    ];

    this.getNodeAttribute = function (nodetype) {
        nodetype = nodetype.trim();
        //console.log('--->>>>>>>'+nodetype)
        //console.log(PROCESSORS_NAME_CATEGORY_MAP)
        var category = 'na'
        if (nodetype in PROCESSORS_NAME_CATEGORY_MAP){
            category = PROCESSORS_NAME_CATEGORY_MAP[nodetype]
        }
        ret =  {
            types: [],
            class: 'defaultnode',
            output: true,
            input: true
        };
        //console.log('>>>>>>>'+category)
        for (var i =0; i < this.nodemap.length; i++) {
            if (this.nodemap[i].category == category) {
                if(nodetype=="dummy_input"){
                    ret =  {
                        types: this.nodemap[i].types,
                        class: this.nodemap[i].class,
                        output: true,
                        input: false
                    };
                }
                else if(nodetype=="dummy_output"){
                    ret =  {
                        types: this.nodemap[i].types,
                        class: this.nodemap[i].class,
                        output: false,
                        input: true
                    };
                }
                else{
                    ret = this.nodemap[i];
                }
                return ret;  // should be reachable.
            }
        }
        console.log('--->>>>>>>'+ret)
        return ret; // actually unreachable.
    };

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
        lineWidth: 3,
        strokeStyle: "#61B7CF",
        joinstyle: "round",
        outlineColor: "white",
        outlineWidth: 2
    }

    // .. and this is the hover style.
    this.connectorHoverStyle = {
        lineWidth: 3,
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
            strokeStyle: "#1cc09f",
            fillStyle: "#ffffff",
            radius: 7,
            lineWidth: 2
        },
        maxConnections: -1,
        isSource: true,
        connector: ["Flowchart", {stub: [20, 20], gap: 10, cornerRadius: 5, alwaysRespectStubs: true}],
        connectorStyle: this.connectorPaintStyle,
        hoverPaintStyle: this.endpointHoverStyle,
        connectorHoverStyle: this.connectorHoverStyle,
        dragOptions: {},
        /*overlays: [
            ["Label", {
                location: [0.5, 1.5],
                label: "Output",
                cssClass: "endpointSourceLabel"
            }]
        ]*/
    }
// the definition of target endpoints (will appear when the user drags a connection)
    this.targetEndpoint = {
        endpoint: "Dot",
        paintStyle: {
            strokeStyle: "#1cc09f",
            fillStyle: "#ffffff",
            radius: 7,
            lineWidth: 2
        },
        hoverPaintStyle: this.endpointHoverStyle,
        maxConnections: -1,
        dropOptions: {hoverClass: "hover", activeClass: "active"},
        isTarget: true,
        /*overlays: [
            ["Label", {location: [0.5, -0.5], label: "Input", cssClass: "endpointTargetLabel"}]
        ]*/
    }

    this.init = function (connection) {
        connection.getOverlay("label").setLabel(connection.sourceId.substring(15) + "-" + connection.targetId.substring(15));
        connection.bind("editCompleted", function (o) {
//            if (typeof console != "undefined")
                //console.log("connection edited. path is now ", o.path);
        });
    };

    this._addEndpoints = function (toId, sourceAnchors, targetAnchors) {
        var tmpEP1 = []
        var tmpEP2 = []

        for (var i = 0; i < sourceAnchors.length; i++) {
            var sourceUUID = toId + sourceAnchors[i];
            //console.log(sourceUUID+"<<<<<<<<<<<<")

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
        ////console.log("CURRENTNODE LEN: "+this.currentNodes.length);
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
        //console.log("Component ID:"+componentID+" | type: "+type);
        //var imageSrc = this.componentImagePath+icon;

        var Div = $('<div>', {id:componentID}, {class: 'window'}).css({
            //border: 'solid 1px',
            top: topPos+'px',
            left: leftPos+'px'
        }).appendTo(this.canvasID);

        $(Div).attr('data-nodetype',type);
        if(argData != null)
            $(Div).attr('arg-data',argData);
        Div.html('' +
        '<i class="fa fa-close window-remover" parentid="'+componentID+'" id="window-remover-01"></i>' +
        '<span class="processor-snippet">'+icon+'</span>');
        var nodeAttr = this.getNodeAttribute(type);
        $(Div).addClass('window');
        $(Div).addClass(nodeAttr.class);
        var inputEndPoint = (nodeAttr.input) ?  ["LeftMiddle"] : [];
        var outputEndPoint = (nodeAttr.output) ?  ["RightMiddle"] : [];
        this._addEndpoints(componentID, outputEndPoint, inputEndPoint);
        instance.draggable(jsPlumb.getSelector(".flowchart-canvas .window"), { grid: [20, 20] });
        //instance.draggable(jsPlumb.getSelector(".flowchart-canvas .window"), { containment: ".flowchart-canvas" });
        // check completness
        this.checkArgData(componentID, type, argData);
    }

    /**
    Check completeness of argument data, in case not complete displaye warning indicator, otherwise remove warning indicator
    */
    this.checkArgData = function(componentID, type, argData) {
        var addwarning = false;
        if (argData != null) {
            argData = $.parseJSON($.base64.decode(argData));
            for (var i = 0; i < argData.length; i++) {
                if (argData[i].is_mandatory !== "" && argData[i].value === "" ) {
                    addwarning = true;
                    break;
                }
            }
        } else {
            try {
                argData = $.parseJSON(SystemComponent.getArgumentsDefinition(type));
                for (var i = 0; i < argData.length; i++) {
                    if (argData[i].is_mandatory == true && !argData[i].value) {
                        addwarning = true;
                        break;
                    }
                }
            } catch (err) {
                addwarning = true;
            }
        }
        if (addwarning) {
            var span = $("#" + componentID + " span");
            $(span).attr('data-toggle', "tooltip");
            $(span).attr('title', 'not completed');
            $(span).tooltip({placement: 'bottom',trigger: 'manual'}).tooltip('show');
            var tooltip = $("#"+ componentID + " .tooltip");
            tooltip.css('left','0px');
        } else {
            $("#"+componentID + " .tooltip").remove();
        }
        return addwarning;
    }

    this.getFlowchartHeight = function(){
        var tallest = -1;
        var MIN = 400;
        var MAX = 700;
        $(".window").each(function (idx, elem){
            var $elem = $(elem)
            //var endpoints = jsPlumb.getEndpoints($elem.attr('id'));
            var tmp = parseInt($elem.css('top'), 10);
            var tmpH = parseInt($elem.css('height'), 10);
            if(tmp > tallest){
                tallest = tmp + tmpH*3.3;
            }
            if (tallest < MIN){
                tallest = MIN;
            }
            if (tallest > MAX){
                tallest = MAX;
            }
        });
        return tallest;
    }

    /**
     * Remove Node from canvas
     * @param nodeID
     */
    this.removeNode = function(nodeID){

        //DELETE DUMMY IO NODE
        var dummyDeletion = nodeID.split("_");
        if (dummyDeletion[1]=='dummy'){
            if(dummyDeletion[2]=='input'){
                dummy_input = false;
            }
            if(dummyDeletion[2]=='output'){
                dummy_output = false;
            }
        }
        // REMOVE RELATED CONNECTION
        $.each(instance.getConnections(), function(idx, connection){
//            console.log(">>>> Connection : "+connection);
            if(connection.targetId == nodeID || connection.sourceId == nodeID) {
                jsPlumb.detach(connection);
            }
        });
        // REMOVE RELATED ENDPOINT
        $.each(this.currentNodes, function (idx, elem){
            ////console.log(elem);
            if(elem.nodeID == nodeID) {
                elem.epSources.forEach(function(ep) {
                    jsPlumb.deleteEndpoint(ep);
                });
                elem.epSources = []
                elem.epOutputs.forEach(function(ep) {
                    jsPlumb.deleteEndpoint(ep);
                });
                elem.epOutputs = []
            }
        });
        // REMOVE NODE
        jsPlumb.remove(nodeID);
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
            //console.log(endpoints);
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
        //console.log(instance.getConnections());
        $.each(instance.getConnections(), function(idx, connection){
            //console.log(connection);
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
        var ask_validate = ask_validate;
        // SAVE TO DOM
        var Div = $('<li>').attr('onclick',"componentProvider.loadFlowchart('"+flowChartJson+"')").html("<a href='#'>"+queryName+"</a>").appendTo(this.queryParentID);

        // SAVE TO BACKEND
        $.ajax({
            type: 'POST',
            url: HOST + '/workspace/streaming-query/save/',
            data: {
                id: queryID,
                name: queryName,
                description: queryDescription,
                data: flowChartJson
            },
            "beforeSend": function(xhr, settings) {
                //console.log("Before Send");
                $.ajaxSettings.beforeSend(xhr, settings);
            },
            success: function (b) {
                if (b && b.id != null) {
                    docControllerCallback.flagAsEditDocument(b.id);
                    $("#save-workflow").html("Save");
                    toastr.success('Workflow "'+queryName+'" saved successfully!', '');
                    drawRecentQueryTable(source_id);
                    reset();

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
        var connections = flowchart.connections;
        var mInstance = this;

        $("#builder-query-name").html(""+wfname);
        $("#builder-query-description").html(""+wfdescription);

        $.each(nodes, function(index, node){
            //console.log(this);
            mInstance.addComponent(node.blockId, node.nodetype, node.positionY, node.positionX, node.snippet, node.argData);
        });


        $.each(nodes, function(index, node){
        if (node.nodetype == 'macro'){
            var obj = $.parseJSON($.base64.decode(node.argData));
            var macroId = obj[0]["value"].split("_")[0];
            var temp = {"selectedProcessor":node.blockId};
            $.ajax({
                    type: 'POST',
                    url: HOST + '/workspace/streaming-query/detail/',
                    data: {
                        id: macroId
                    },
                    "beforeSend": function(xhr, settings) {
                        $.ajaxSettings.beforeSend(xhr, settings);
                    },
                    success: function (b) {
                        node.snippet = b.name;
                        //console.log("Workflow data loaded");
                        if (b && b.status == null) {
                            //Parse query to check dummy_input & dummy_output
                            var content = $.parseJSON(b.data);
                            var input = false;
                            var output = false;
                            for (var i=0;i<content['nodes'].length;i++){
                                if (content['nodes'][i]['nodetype'] == 'dummy_input'){
                                    input = true;
                                }
                                else if (content['nodes'][i]['nodetype'] == 'dummy_output'){
                                    output = true;
                                }
                            }
                            var nodeID = temp['selectedProcessor'];
                            $("#"+nodeID).find(".processor-snippet").html(b.name);
                                // REMOVE RELATED ENDPOINT
                                $.each(componentProvider.currentNodes, function (idx, elem){
                                    //console.log(elem);
                                    if(elem.nodeID == nodeID) {
                                        //console.log("REMOVED ENDPOINT : " + elem.nodeID);
                                        elem.epSources.forEach(function(ep) {
                                            jsPlumb.deleteEndpoint(ep);
                                            console.log(ep);
                                        });
                                        elem.epSources = []
                                        elem.epOutputs.forEach(function(ep) {
                                            jsPlumb.deleteEndpoint(ep);
                                            console.log(ep);
                                        });
                                        elem.epOutputs = []
                                    }
                                });
                            if (input){
                                componentProvider._addEndpoints(temp['selectedProcessor'], [], ["LeftMiddle"]);
                            }
                            if (output){
                                componentProvider._addEndpoints(temp['selectedProcessor'],["RightMiddle"], []);
                            }
                        }
                        $.each(connections, function( index, elem ) {
                        if (elem.pageSourceId.indexOf("macro") || elem.pageTargetId.indexOf("macro")){
                            instance.connect({uuids:[elem.pageSourceId+"RightMiddle", elem.pageTargetId+"LeftMiddle"], editable:true});
                            }
                        });
                        instance.repaintEverything();
                    },
                    error: function (e) {
                        console.log(e)
                        }
                });
            }
        });

        $.each(connections, function( index, elem ) {
            if (elem.pageSourceId.indexOf("macro")==-1 && elem.pageTargetId.indexOf("macro")==-1){
                instance.connect({uuids:[elem.pageSourceId+"RightMiddle", elem.pageTargetId+"LeftMiddle"], editable:true});
            }
        });
        docControllerCallback.flagAsEditDocument(wfid, wfname);
    }

    this.loadWorkflow = function(queryID, docControllerCallback){
        console.log("WFID : "+queryID)
        var parent = this;
        $.ajax({
            type: 'POST',
            url: HOST + '/workspace/streaming-query/detail/',
            data: {
                id: queryID
            },
            "beforeSend": function(xhr, settings) {
                $.ajaxSettings.beforeSend(xhr, settings);
            },
            success: function (b) {
                //console.log("Workflow data loaded");
                if (b && b.status == null) {
                    //console.log(b);
                    //Parse query to check dummy_input & dummy_output
                    var content = $.parseJSON(b.data);
                    for (var i=0;i<content['nodes'].length;i++){
                        if (content['nodes'][i]['nodetype'] == 'dummy_input'){
                            dummy_input = true;
                        }
                        else if (content['nodes'][i]['nodetype'] == 'dummy_output'){
                            dummy_output = true;
                        }
                    }
                    parent.drawWorkflow(b.id, b.name, b.description, b.data, docControllerCallback);
                    $("#save-workflow").html("Save");
                    docControllerCallback.resizeFitCanvas(parent.getFlowchartHeight());

                } else if(b.message != null){
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
            //console.log("connection " + connection.id + " is being dragged. suspendedElement is ", connection.suspendedElement, " of type ", connection.suspendedElementType);
        });

        instance.bind("connectionDragStop", function(connection) {
            //console.log("connection " + connection.id + " was dragged");
        });

        instance.bind("connectionMoved", function(params) {
            //console.log("connection " + params.connection.id + " was moved");
        });
    });

    jsPlumb.fire("jsPlumbDemoLoaded", instance);

});

var componentProvider = new ComponentProvider();
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

                if (icon=="dummy_input" && dummy_input){
                    toastr.warning("Only 1 dummy_input allowed","dummy_input already exist!");
                }
                else if (icon=="dummy_output" && dummy_output){
                    toastr.warning("Only 1 dummy_output allowed","dummy_output already exist!");
                }
                else{
//                    if(icon !=undefined){
//                        console.log("ID & icon : " + draggedId + " " + icon);
//                    }
                    var seg = draggedId.split("-");
                    if (seg.length != 0 && seg[0] == ("component")) {
                        var $newPosX = ui.offset.left - $(this).offset().left+$(this).scrollLeft();
                        var $newPosY = ui.offset.top - $(this).offset().top+$(this).scrollTop();
                        componentProvider.addNewComponent(seg[1], $newPosY, $newPosX, icon);
                        if (icon=="dummy_input"){dummy_input=true;}
                        if (icon=="dummy_output"){dummy_output=true;}
                    }
                }
            }catch(err){
                console.log(err.message);
            }
        }
    });


    // SAVE & LOAD DESIGNED QUERY
    $("#save-query").click(function(){
        componentProvider.saveFlowchart();
    });




});
