/**
 * Created by SRIN on 2/25/2015.
 */
var DocController;
var numOfWorkers = 1;
var resizeNumOfWorkers = function(nw){
    numOfWorkers = nw;
}
var loggingMode = "verbose";
$(document).ready(function () {
    var selectedProcessor = null;
    var mArgumentModalWindow = $("#myModal");
    var defaultWFName = "New Query"
    var defaultWFDescription = "This is new query"
    var buttonSaveAs = "Save as query";
    // Load UI Definitions
    //ArgumentLoader.init();

    DocController = {
        validated : false,
        compiled : false,
        launched : false,
        isRenameReqiured : function ()
        {
            var obj = $("#builder-query-name");
            return (!obj.hasClass("new-ready"));
        },
        flagAsNewDocument :function() {
            var obj = $("#builder-query-name");
            obj.addClass("new-wf");
            obj.removeClass("new-ready");
            obj.attr("data_id", 0);
            obj.html(defaultWFName);
            $("#builder-query-description").html(defaultWFDescription);
            $("#save-workflow").html(buttonSaveAs);
        },
        flagAsNewDocumentWithNameNoRequired : function() {
            var obj = $("#builder-query-name");
            obj.addClass("new-wf");
            obj.addClass("new-ready");
            obj.attr("data_id", 0);
        },
        flagAsDocumentWithNameNoRequired : function() {
            var obj = $("#builder-query-name");
            obj.addClass("new-ready");
        },
        flagAsEditDocument : function(id) {
            var obj = $("#builder-query-name");
            obj.removeClass("new-wf");
            obj.removeClass("new-ready");
            obj.attr("data_id", id);
        },
        flagAsEditDocument : function(id, wfname) {
            var obj = $("#builder-query-name");
            obj.removeClass("new-wf");
            obj.removeClass("new-ready");
            obj.attr("data_id", id);
            $("#builder-query-name").html(wfname);
        },
        renameWorkflow : function(queryID, queryName, queryDescription, isUpdate){
            var parent = this;
            bootbox.setDefaults("animate", false);
            if (queryID==0) {
                placeholderQueryName = "placeholder='"+queryName+"'";
                queryDescription = "";
            } else {
                placeholderQueryName = "value='"+queryName+"'";
            }
            if ( loggingMode == "verbose" ) {
                loggingModeButtonHtml = '<div class="radio i-checks"> <label> <input type="radio" value="" name="loggingMode"> <i></i>Logging Off</label>'+
                            '<label> <input type="radio" value="" name="loggingMode"> <i></i>Smart Logging</label> '+
                            '<label> <input type="radio" value="" name="loggingMode" checked> <i></i>Verbose Mode</label> </div>';
            } else if ( loggingMode == "smart" ) {
                loggingModeButtonHtml = '<button type="button" class="btn btn-outline btn-primary btn-sm">No Logging</button> '+
                            '<button type="button" class="btn btn-success btn-sm">Smart Mode</button> '+
                            '<button type="button" class="btn btn-outline btn-danger btn-sm">Verbose Mode</button>';
            } else {
                loggingModeButtonHtml = '<button type="button" class="btn btn-primary btn-sm">No Logging</button> '+
                            '<button type="button" class="btn-outline btn-success btn-sm">Smart Mode</button> '+
                            '<button type="button" class="btn-outline btn-danger btn-sm">Verbose Mode</button>';
            }
            bootbox.dialog({
                title: "Streaming Query - Choose Query Name!",
                message: '<div class="row">  ' +
                    '<div class="col-md-12"> ' +
                    '<form class="form-horizontal"> ' +
                    '<div class="form-group"> ' +
                    '<label class="col-md-3 control-label" for="name">Name</label> ' +
                    '<div class="col-md-9"> ' +
                    '<input id="bootbox-query-name" name="name" type="text" '+placeholderQueryName+' class="form-control input-md"> ' +
                    '<span class="help-block">Please choose a name</span> </div> ' +
                    '</div> ' +
                    '<div class="form-group"> ' +
                    '<label class="col-md-3 control-label" for="description">Description</label> ' +
                    '<div class="col-md-9"> ' +
                    '<textarea id="bootbox-query-description" rows=3 name="description" placeholder="This is new streaming query" type="text" class="form-control input-md">'+queryDescription+'</textarea> ' +
                    '<span class="help-block">Detailed description helps more effective query development and maintenance</span> </div> ' +
                    '</div> ' +
                    '<div class="form-group"> ' +
                    '<label class="col-md-3 control-label" for="numOfWorkers">Number Of Workers</label> ' +
                    '<div class="col-md-9"> ' +
                    '<span id="ionrange_4"></span> ' +
                    '<span class="help-block">Please give an integer to launch the equivalent number of workers for parallelism</span> </div> ' +
                    '</div> ' +
                    '<div class="form-group"> ' +
                    '<label class="col-md-3 control-label" for="runningMode">Logging Level</label> ' +
                    '<div class="col-md-9"> ' +
                    loggingModeButtonHtml +
                    '<span class="help-block">Smart mode: debugging information from WARN to CRIT <p>Verbose mode: all debugging information from INFO to CRIT</span> </div>'+
                    '</div> ' +
                    '</div> </div>' +
                    '</form> </div>  </div>' +
                    '<script> '+
                    '$("#ionrange_4").ionRangeSlider({ min: 1, max: 4, type: "single", step: 1, prettify: false, hasGrid: true, '+
                    'from: '+numOfWorkers+', '+
                    'onChange: function(obj){ resizeNumOfWorkers(obj.from); } '+
                    '}); '+
                    '$("input").iCheck({radioClass: "iradio_square-green", handle: "radio"}); ' +
                    '</script>',
                buttons: {
                    success: {
                        label: "Save",
                        className: "btn-success",
                        callback: function () {
                            var name = $('#bootbox-query-name').val();
                            var description = $('#bootbox-query-description').val();
                            if (name==="") name="New Query";
                            if (description==="") description="This is new query";
                            console.log(name+","+description);
                            $("#builder-query-name").html(name);
                            $("#builder-query-description").html(description);
                            var dataID = $("#builder-query-name").attr("data_id");
                            if (!isUpdate){
                                parent.flagAsNewDocumentWithNameNoRequired();
                            }
                            componentProvider.saveFlowchart(queryID, name, description, parent);
                        }
                    },
                    cancel: {
                        label: "Cancel",
                        className: "btn-cancel"
                    }
                }
            });
        },
        resizeFitCanvas : function(h){
            $("#top-page").css('height',h);
        },
        retrieveKafkaTopicList: function(flowchartJson) {
            //console.log("-- retrieveKafkaTopicList > begin --");
            var flowchart = JSON.parse(flowchartJson);
            var nodes = flowchart.nodes;

            var topicList = [];
            $.each(nodes, function(index, node) {
                if (node.nodetype.indexOf("kafka") > -1) {
                    var currData = $.parseJSON($.base64.decode(node.argData));
                    var kafka = {};
                    for (var i = 0; i < currData.length; i++) {
                        var row = currData[i];
                        if (row.name == "topic_name") {
                            kafka.topic = row.value;
                        } else if (row.name == "kafka_server") {
                            kafka.server = row.value;
                        }
                    }

                    topicList.push(kafka.server+ "#" + kafka.topic);
                }
            });
            //console.log(topicList);
            //console.log("-- retrieveKafkaTopicList > end --");

            return topicList;
        }

    }

    // On Click Event
    $("#flowchart-canvas").on('click', ".window", function(e){
        var group = e.currentTarget.attributes["data-nodetype"].value;
        selectedProcessor = e.currentTarget.attributes["id"].value
        //console.log("Selected Processor = "+selectedProcessor);
        get_help_doc(selectedProcessor)
    });


    // On DoubleClick Event
    $("#flowchart-canvas").on('dblclick', ".window", function(e){
        var group = e.currentTarget.attributes["data-nodetype"].value;

        selectedProcessor = e.currentTarget.attributes["id"].value;
        //console.log("Selected Processor = "+selectedProcessor);
        mArgumentModalWindow.find(".modal-title").html(group);
        ko.cleanNode;

        if (group == "dummy_output" || group == "dummy_input")
        {
        //Do something if dummy_input/output dbl clicked
        }
        else
        {
        var orgData = $.parseJSON(SystemComponent.getArgumentsDefinition(group));
        //console.log(orgData);
        if(null != orgData) {
            $("#for-delete-query-id").remove();
            $("#for-delete-link").remove();
            var currData = $("#"+selectedProcessor).attr('arg-data');
            if(currData != null) {
                currData = $.parseJSON( $.base64.decode(currData) );
                for (var i = 0; i < currData.length; i++) {
                    var row = currData[i];
                    //console.log(row);
                    if (row.name == orgData[i].name) {
                        orgData[i].value = row.value
                    }
                }
            }else{
                console.log("Set default values on new component");

                for (var i = 0; i < orgData.length; i++) {
                    var row = orgData[i];
                    if (row.default != "ND") {
                        row.value = row.default;
                    }
                }
            }
            if ($("#"+selectedProcessor).attr('data-nodetype')=='macro'){
                var currID = '';
                //init value, data-binder.js for dropdown update value
                if (currData!=null){
                    currID = currData[0].value.split("_")[0];
                }
                $("#target-argument-form").append("<div id='for-delete-query-id' class='form-group'><label style='text-align:left' class='col-sm-2 control-label'>query_id</label><h4 class='col-sm-9' id='additional-info-query-id'>"+currID+"</h4></div>");
                $("#target-argument-form").append("<div id='for-delete-link' class='form-group'><div class='col-sm-12'><a style='position:relative;top:14px;text-align:left' id='additional-info-link' href='?wfid="+currID+"' target='_blank'>Click here to view the query in a new tab</a></div></div>");
            }
            var mappedTasks = $.map(orgData, function (item) {
                return new ArgumentModel(item)
            });
            tlvm.tasks(mappedTasks);
        }
        mArgumentModalWindow.modal('show');
        }
    });

    /* newly added to provide removal feature on processor node*/
    $("#flowchart-canvas").on('click', ".window-remover", function(e){
        console.log(e);
        if(confirm("Remove node?")){
            var nodeID = e.currentTarget.attributes["parentid"].value;
            componentProvider.removeNode(nodeID);
        }
    });



    mArgumentModalWindow.on('hidden.bs.modal', function () {
        selectedProcessor = null;
    })

    $("#btn-modal-save").click(function(e){
        tlvm.getMinifiedJson();
        if(selectedProcessor != null){
            $("#"+selectedProcessor).attr('arg-data', $.base64.encode( tlvm.lastSavedJson().toString() ));
            // check whether all required argument set (remove/add warning if apply)
            var obj = JSON.parse(tlvm.lastSavedJson().toString());
            if (obj[0]["name"]=="macro_name"){
                $("#"+selectedProcessor).find(".processor-snippet").html(obj[0]["value"].split("_")[1]);
                var macroId = obj[0]["value"].split("_")[0];
                var temp = {"selectedProcessor":selectedProcessor};
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
                        console.log("Workflow data loaded");
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
//                                $.each(instance.getConnections(), function(idx, connection){
//                                    if(connection.targetId == nodeID || connection.sourceId == nodeID){
//                                        jsPlumb.detach(connection);
//                                    }
//                                });
                                // REMOVE RELATED ENDPOINT
                                $.each(componentProvider.currentNodes, function (idx, elem){
                                    //console.log(elem);
                                    if(elem.nodeID == nodeID) {
                                        if (input==false && output==false){
                                        elem.epSources.forEach(function(ep) {
                                            instance.deleteEndpoint(ep);
                                            console.log(ep);
                                        });
                                        elem.epSources = []
                                        elem.epOutputs.forEach(function(ep) {
                                            instance.deleteEndpoint(ep);
                                            console.log(ep);
                                        });
                                        elem.epOutputs = []
                                        }
                                        else if (output==false){
                                        elem.epSources.forEach(function(ep) {
                                            instance.deleteEndpoint(ep);
                                            console.log(ep);
                                        });
                                        elem.epSources = []
                                        }
                                        else if (input==false){
                                        elem.epOutputs.forEach(function(ep) {
                                            instance.deleteEndpoint(ep);
                                            console.log(ep);
                                        });
                                        elem.epOutputs = []
                                        }
                                    }
                                });
                            if (input){
                                componentProvider._addEndpoints(temp['selectedProcessor'], [], ["LeftMiddle"]);
                            }
                            if (output){
                                componentProvider._addEndpoints(temp['selectedProcessor'],["RightMiddle"], []);
                            }
                            instance.repaintEverything();
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
            componentProvider.checkArgData(selectedProcessor, $("#"+selectedProcessor).attr('data-nodetype'), $.base64.encode( tlvm.lastSavedJson().toString() ));
        }
        mArgumentModalWindow.modal('hide');
        DocController.flagAsDocumentWithNameNoRequired();
        var name = $("#builder-query-name");
        var description = $("#builder-query-description");
        var queryID =  name.attr("data_id");
        var isUpdate = true;
        if( $("#save-workflow").html() == buttonSaveAs){
            isUpdate = false;
            DocController.renameWorkflow(0, defaultWFName, defaultWFDescription, isUpdate);
        } else if( (queryID == null || queryID <= 0) && DocController.isRenameReqiured()) {
            // NEW DESIGN
            isUpdate = false;
            DocController.renameWorkflow(0, defaultWFName, defaultWFDescription, isUpdate);
        }else{
            componentProvider.saveFlowchart(queryID, name.html(), description.html(), DocController);
        }
    });

    $("#save-workflow").click(function (e) {
        var name = $("#builder-query-name");
        var description = $("#builder-query-description");
        var queryID =  name.attr("data_id");
        var isUpdate = true;
        if( $("#save-workflow").html() == buttonSaveAs ){
            isUpdate = false;
            DocController.renameWorkflow(0, defaultWFName, defaultWFDescription, isUpdate);
        } else if( (queryID == null || queryID <= 0) && DocController.isRenameRequired()) {
            // NEW DESIGN
            isUpdate = false;
            DocController.renameWorkflow(0, defaultWFName, defaultWFDescription, isUpdate);
        }else{
            componentProvider.saveFlowchart(queryID, name.html(), description.html(), DocController);
        }
    });

    $("#builder-query-name").click(function () {
        var name = $(this);
        var description = $("#builder-query-description").html();
        var queryID =  name.attr("data_id");
        var isUpdate = true;
        if (queryID == null || queryID <= 0) isUpdate = false;
        DocController.renameWorkflow(queryID, name.html(), description, isUpdate); // Rename Locally Only
    });

    $("#builder-query-description").click(function () {
        var name = $("#builder-query-name");
        var description = $(this).html();
        var queryID =  name.attr("data_id");
        var isUpdate = true;
        if ( queryID == null || queryID <= 0 ) isUpdate = false;
        DocController.renameWorkflow(queryID, name.html(), description, isUpdate); // Rename Locally Only
    });

    var newworkflow = function(e) {
        flowchartInputId = '';
        flowchartOutputId = '';
        console.log('reset clicked');
        //jsPlumb.reset();
        instance.reset();
        $.each(instance.getConnections(), function (idx, connection) {
            jsPlumb.detach(connection);
        });
        componentProvider.clearNodesData();
        $("#flowchart-canvas").empty();
        $(this).addClass('active').siblings().removeClass('active');
        DocController.flagAsNewDocument();
        reset();
    };

    $("#new-workflow").click(newworkflow);
    $("#top-page").resizable({
        handles: 's',
        resize: function(event, ui) {

        }
    });



    /*
    Load query from json file
    */
    $("#load-from-file").on("change", function(evt) {
        var files = evt.target.files;
        var reader = new FileReader();

        // onload handler for getting the file content.
        reader.onload = function(theFile) {
            //console.log(theFile.target.result);
            var b = $.parseJSON(theFile.target.result);
            newworkflow(null);
            componentProvider.drawWorkflow(b.id, b.name, b.description, b.data, DocController);
            DocController.resizeFitCanvas(componentProvider.getFlowchartHeight());
            DocController.flagAsNewDocument();
        };

        reader.readAsText(files[0]);
    });

});


function get_help_doc(selectedProcessor){
    var regex = /(?:^|\s)flowchart_(.*)_(?:\d+|$)/g;
    var match = regex.exec(selectedProcessor);
    var command_id = match[1]
    $.ajax({
        type: 'GET',
        url: help_doc_url+'?command_id='+command_id,
        "beforeSend": function(xhr, settings) {
            $.ajaxSettings.beforeSend(xhr, settings);
        },
        success: function (result) {
            $('#help_panel').html(result);
        },
        error: function (e) {
            console.log(e)
        }
    });
 }
