/**
 * Created by SRIN on 2/25/2015.
 */

$(document).ready(function () {
    var selectedProcessor = null;
    var mArgumentModalWindow = $("#myModal");
    var defaultWFName = "New Query"
    var defaultWFDescription = "This is new query"
    // Load UI Definitions
    //ArgumentLoader.init();

    var DocController = {
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
            $("#save-workflow").html("Save as...");
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
                placeholderQueryDescription = "placeholder='"+queryDescription+"'";
            } else {
                placeholderQueryName = "value='"+queryName+"'";
                placeholderQueryDescription = "value='"+queryDescription+"'";
            }
            bootbox.dialog({
                title: "Add Data - Choose ETL Query Name!",
                message: '<div class="row">  ' +
                    '<div class="col-md-12"> ' +
                    '<form class="form-horizontal"> ' +
                    '<div class="form-group"> ' +
                    '<label class="col-md-3 control-label" for="name">Name</label> ' +
                    '<div class="col-md-6"> ' +
                    '<input id="bootbox-query-name" name="name" type="text" '+placeholderQueryName+' class="form-control input-md"> ' +
                    '<span class="help-block">Please choose a name</span> </div> ' +
                    '</div> ' +
                    '<div class="form-group"> ' +
                    '<label class="col-md-3 control-label" for="description">Description</label> ' +
                    '<div class="col-md-9"> ' +
                    '<input id="bootbox-query-description" name="description" type="text" '+placeholderQueryDescription+' class="form-control input-md"> ' +
                    '<span class="help-block">Detailed description helps more effective query development and maintenance</span> </div> ' +
                    '</div> ' +
                    '</div> </div>' +
                    '</form> </div>  </div>',
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
                            c.saveFlowchart(queryID, name, description, parent);
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
            console.log("Height: "+h);
            $("#top-page").css('height',h);
        }


    }

    // On DoubleClick Event
    $("#flowchart-canvas").on('dblclick', ".window", function(e){
        console.log(e.currentTarget.attributes);
        var group = e.currentTarget.attributes["data-nodetype"].value;
        selectedProcessor = e.currentTarget.attributes["id"].value
        console.log("Selected Processor = "+selectedProcessor);
        mArgumentModalWindow.find(".modal-title").html(group);
        ko.cleanNode;

        var orgData = $.parseJSON(SystemComponent.getArgumentsDefinition(group));
        if(null != orgData) {
            var currData = $("#"+selectedProcessor).attr('arg-data');
            if(currData != null) {
                currData = $.parseJSON( $.base64.decode(currData) );
                for (var i = 0; i < currData.length; i++) {
                    var row = currData[i];
                    console.log(row);
                    if (row.name == orgData[i].name) {
                        orgData[i].value = row.value
                    }
                }
            }else{
                console.log("#No 'arg-data' found!");
            }
            var mappedTasks = $.map(orgData, function (item) {
                return new ArgumentModel(item)
            });
            tlvm.tasks(mappedTasks);
        }
        mArgumentModalWindow.modal('show');
    });

    /* newly added to provide removal feature on processor node*/
    $("#flowchart-canvas").on('click', ".window-remover", function(e){
        console.log(e);
        if(confirm("Remove node?")){
            var nodeID = e.currentTarget.attributes["parentid"].value;
            c.removeNode(nodeID);
        }
    });



    mArgumentModalWindow.on('hidden.bs.modal', function () {
        selectedProcessor = null;
    })

    $("#btn-modal-save").click(function(e){
        tlvm.getMinifiedJson();
        if(selectedProcessor != null){
            $("#"+selectedProcessor).attr('arg-data', $.base64.encode( tlvm.lastSavedJson().toString() ));
        }
        mArgumentModalWindow.modal('hide');
        DocController.flagAsDocumentWithNameNoRequired();
    });

    $("#save-workflow").click(function (e) {
        var name = $("#builder-query-name");
        var description = $("#builder-query-description");
        var queryID =  name.attr("data_id");
        var isUpdate = true;
        if( (queryID == null || queryID <= 0) && DocController.isRenameReqiured()) {
            // NEW DESIGN
            isUpdate = false;
            DocController.renameWorkflow(0, defaultWFName, defaultWFDescription, isUpdate);
        }else{
            c.saveFlowchart(queryID, name.html(), description.html(), DocController);
        }
    });

    $("#builder-query-name").click(function () {
        var name = $(this);
        var description = $("#builder-query-description").html();
        var queryID =  name.attr("data_id");
        var isUpdate = true;
        if ( queryID == null || queryID <= 0 ) isUpdate = false;
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

    $("#new-workflow").click(function (e) {
        console.log('reset clicked');
        jsPlumb.reset();

        $.each(instance.getConnections(), function (idx, connection) {
            jsPlumb.detach(connection);
        });

        c.clearNodesData();

        $("#flowchart-canvas").empty();
        $(this).addClass('active').siblings().removeClass('active');

        DocController.flagAsNewDocument();
    });

    $("#top-page").resizable({
        handles: 's',
        resize: function(event, ui) {

        }
    });


    if(getURLParameterByName("wfid")!=null){
        var queryName = getURLParameterByName("wfid");
        //console.log("Loading Query Name:"+queryName);
        c.loadWorkflow(queryName, DocController);
    }else{
        DocController.flagAsNewDocument();
    }
});