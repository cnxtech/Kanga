var tapped = false;
var callabck_launch = false;
var callabck_remote_launch = false;
var createCode;

function mvn_validate(){
    DocController.validated = false;
    DocController.launched = false;
    validate(DocController);
}
function mvn_launch(){
    DocController.launched = false;
    if (DocController.validated == false){
        callabck_launch = true;
        validate(DocController);
    }else{
        launch(DocController);
    }
}
function mvn_remote_launch(ip){
    DocController.launched = false;
    if (DocController.validated == false){
        callabck_remote_launch = true;
        validate(ip);
    }
    else{
        remote_launch(ip);
    }
}

function validate(ip){
    $("#tab-2").html("<div class='animated fadeInRight'><pre>The given query is being validated.<i class='fa fa-refresh fa-spin'></i></pre></div>");
    activaTab('tab-2');
    var queryID = $("#builder-query-name").attr("data_id");
    var current_validate_url = validate_url+"/"+queryID+"/";
    $.ajax({
        url: current_validate_url,
        timeout: 30000,
        success: function(json) {
            var msg = "";
            var success_msg = "";
            var node_code = "";
            var intermediate_query = "";
            var cmd = "";
            if (json['error_message']!="") {
                msg = '<div><pre style="overflow:auto;  font-size:10px; background-color: #f2dede;   border-color: #ebccd1; color: #a94442;">'+json['error_message']+'</pre></div>';
            }
            else if (json['success_message']!="") {
                msg = '<div class="alert alert-success">'+json['success_message']+'</div>';
            }
            if (json['node_code']!="") {
                node_code = '<div><pre style="overflow:auto;  font-size:10px; background-color: #d9edf7;   border-color: #bce8f1; color: #31708f;">'+json['node_code']+'</pre></div>';
            }
            if (json['intermediate_query']!="") {
//                intermediate_query = '<div class="alert alert-warning"><pre style="overflow:auto; height:500px;">'+JSON.stringify(json['intermediate_query'],null,4)+'</pre></div>';
                intermediate_query = '<div><pre style="overflow:auto;  font-size:10px;">'+JSON.stringify(json['intermediate_query'],null,4)+'</pre></div>';
            }
            $("#tab-2").html("<div class='animated fadeInRight'>"+
                              msg+
                              node_code
                              );
            $("#tab-3").html("<div class='animated fadeInRight'>"+
                              msg+
                              intermediate_query
                              );
            if (json['result']==true){
                createCode = json['node_code'];
                bvm.successValidateButton();
                DocController.validated = true;
                if (callabck_launch) {
                    callabck_launch = false;
                    launch();
                }
                else if(callabck_remote_launch){
                    callabck_remote_launch = false;
                    remote_launch(ip);
                }
            }else{
                bvm.failureValidateButton();
                DocController.validated = false;
                callabck_launch = false;
            }
        },
        error: function (xhr, ajaxOptions, thrownError) {
            alert(xhr.status);
            alert(thrownError);
        },
        complete: function(jqXHR) {
            console.log(jqXHR);
        },
        dataType:"json",
    });
}

function launch(){
    $("#tab-3").html("<div class='animated fadeInRight'><pre>Launching is being prepared.<i class='fa fa-refresh fa-spin'></i></pre></div>");
    activaTab('tab-3');
    var queryID = $("#builder-query-name").attr("data_id");
    var current_launch_url = launch_url+"/"+queryID+"/"
    console.log(current_launch_url);
    if ( DocController.validated == false) {
        mvn_validate();
        callabck_launch = true;
    }else{
        $.ajax({
            url: current_launch_url,
            timeout: 30000,
            success: function(json) {
                var msg = "";
                var stdout = "";
                if (json['error_message']!="") {
                    msg = '<div><pre style="overflow:auto;  font-size:10px; background-color: #f2dede;   border-color: #ebccd1; color: #a94442;">'+json['error_message']+'</pre></div>';
                }
                else if (json['success_message']!="") {
                    msg = '<div class="alert alert-success">'+json['success_message']+'</div>';
                }
                if (json['stdout']!="") {
                    stdout = '<div><pre style="overflow:auto;  font-size:10px; background-color: #d9edf7;   border-color: #bce8f1; color: #31708f;">'+json['stdout']+'</pre></div>';
                }
                $("#tab-3").html("<div class='animated fadeInRight'>"+
                                  msg+
                                  stdout
                                  );
                if (json['result']==true){
                    bvm.successLaunchButton();
                    launched = true;
                }else{
                    bvm.failureLaunchButton();
                    launched = false;
                }
            },
            error: function (xhr, ajaxOptions, thrownError) {
                alert(xhr.status);
                alert(thrownError);
            },
            complete: function(jqXHR) {
                console.log(jqXHR);
            },
            dataType:"json",
        });
    }
}

function remote_launch(ip){
    $("#tab-3").html("<div class='animated fadeInRight'><pre>Launching is being prepared.<i class='fa fa-refresh fa-spin'></i></pre></div>");
    activaTab('tab-3');
    var queryID = $("#builder-query-name").attr("data_id");
    var topology_name = 'KangaTopology'+queryID;
    if ( DocController.validated == false) {
        mvn_validate();
        callabck_remote_launch = true;
    }
    else{
        $.ajax({
            type: 'POST',
            url: 'http://'+ip +':8888/topology/',
            data: {
                id: topology_name,
                code : createCode
            },
            timeout: 60000,
            dataType:"json",
            success: function (json) {
                var msg = "";
                var stdout = "";
                var success_msg = 'Kanga successfully launches the topology into '+ ip;
                var error_msg = 'Topology submission failed in ' + ip;

                if (json['result']!="success") {
                    msg = '<div><pre style="overflow:auto;  font-size:10px; background-color: #f2dede;   border-color: #ebccd1; color: #a94442;">'+ error_msg+'</pre></div>';
                }
                else {
                    msg = '<div class="alert alert-success">'+success_msg+'</div>';
                }
                if (json['stdout']!="") {
                    stdout = '<div><pre style="overflow:auto;  font-size:10px; background-color: #d9edf7;   border-color: #bce8f1; color: #31708f;">'+json['description']+'</pre></div>';
                }
                $("#tab-3").html("<div class='animated fadeInRight'>"+
                                  msg+
                                  stdout
                                  );

                if (json['result']=='success'){
                    bvm.successLaunchButton();
                    launched = true;
                }else{
                    bvm.failureLaunchButton();
                    launched = false;
                }
            },
            error: function (xhr, ajaxOptions, thrownError) {
                console.log(xhr);
                console.log(ajaxOptions);
                console.log(thrownError);

                var error_msg = 'Topology submission failed in ' + ip;
                var stdout = stdout = '<div><pre style="overflow:auto;  font-size:10px; background-color: #d9edf7;   border-color: #bce8f1; color: #31708f;">'+ thrownError +'</pre></div>';
                var msg = '<div><pre style="overflow:auto;  font-size:10px; background-color: #f2dede;   border-color: #ebccd1; color: #a94442;">'+ error_msg+'</pre></div>';
                $("#tab-3").html("<div class='animated fadeInRight'>"+ msg + stdout);


            },
            complete: function(jqXHR) {
                console.log(jqXHR);
            }
        });
    }
}



function tap_on(){
    connect();
}
function tap_off(){
    disconnect();
}


function handleAjaxError( xhr, textStatus, error ) {
    if ( textStatus === 'timeout' ) {
        alert( 'The server took too long to send the data.' );
    }
    else {
        alert( 'An error occurred on the server. Please try again in a minute.' );
    }
}
function activaTab(tab){
    $('.nav-tabs a[href="#' + tab + '"]').tab('show');
};

