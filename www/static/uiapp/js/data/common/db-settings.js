function bootbox_db_settings(service_code) {
    bootbox.setDefaults("animate", true);
    var options = "";
    for( var i = 0; i < service.length ; i++){
        options = options +'<option value="' + service[i] +'"> ' + service[i] + '</option>';
    }
    bootbox.dialog({
        title: service_code + " Connection - DB Settings",
        message: '<div class="row">  ' +
            '<div class="col-md-12"> ' +
            '<form class="form-horizontal"> ' +
            '<div class="form-group"> ' +

            '<label class="col-md-3 control-label" for="name">Service: </label> ' +
            '<div class="col-md-9"> ' +
            '<select data-placeholder="Choose a service..." id="bootbox-service-select"> ' +
            '<option value=""> </option>' +
            options +
            '</select>'+
            '<span class="help-block">Please choose db service</span> </div> ' +
            '<label class="col-md-3 control-label" for="bootbox-connection-name">Connection name: </label> ' +
            '<div class="col-md-9"> ' +
            '<input id="bootbox-connection-name" type="text" placeholder="Input connection name" class="form-control input-md"> ' +
            '<span class="help-block">Please provide DB connection name</span> </div> ' +
            '<label class="col-md-3 control-label" for="bootbox-db-name">Database name: </label> ' +
            '<div class="col-md-9"> ' +
            '<input id="bootbox-db-name" type="text" placeholder="Input database name" class="form-control input-md"> ' +
            '<span class="help-block">If db is SQLite, please provide full path of DB file (e.g. c:/example.db)</span> </div> ' +
            '<label class="col-md-3 control-label" for="bootbox-db-user">Database name: </label> ' +
            '<div class="col-md-9"> ' +
            '<input id="bootbox-db-user" type="text" placeholder="Input user name" class="form-control input-md"> ' +
            '<span class="help-block">Please provide database user name</span> </div> ' +
            '<label class="col-md-3 control-label" for="bootbox-db-password">Database name: </label> ' +
            '<div class="col-md-9"> ' +
            '<input id="bootbox-db-password" type="password" placeholder="Input password" class="form-control input-md"> ' +
            '<span class="help-block">Please provide database password</span> </div> ' +
            '</div> ' +
            '</form> </div>  </div>' +
            '<script>'+
            '$("#bootbox-service-select").chosen();'+
            '</script>',

        buttons: {
            success: {
                label: "Save",
                className: "btn-success",
                callback: function () {
                    var service_name = $('#bootbox-service-select').val();
                    var connection_name = $('#bootbox-connection-name').val();
                    var db_name = $('#bootbox-db-name').val();
                    var db_user = $('#bootbox-db-user').val();
                    var db_password = $('#bootbox-db-password').val();
                    ajax_set_DBconnect(service_name,connection_name,db_name,db_user,db_password);
                }
            },
            cancel: {
                label: "Cancel",
                className: "btn-cancel"
            }
        }
    });
}

function ajax_set_DBconnect(service_name,connection_name,db_name,db_user,db_password){
    $.ajax({
        type: 'POST',
        url: db_setting_update_url,
        data: {
            service_name: service_name,
            connection_name: connection_name,
            db_name: db_name,
            db_user: db_user,
            db_password: db_password
        },
        success: function (json) {
            if (json.status=='ok'){
                init_db_schema(connection_name);
                table.ajax.reload();
                toastr.success(json.message,json.status);
            }
            else {
                toastr.error(json.message,'Failed');
            }
        },
        error: function (xhr, ajaxOptions, thrownError) {
            toastr.error(thrownError,'Failed');
        },
        complete: function(jqXHR) {
            console.log(jqXHR);
        },
        dataType:"json",
    });
}


function init_db_schema(connection_name){
    $.ajax({
        type: 'POST',
        url: db_schema_url,
        data: {
            connection_name : connection_name
        },
        "beforeSend": function(xhr, settings) {
            console.log("Before Send");
            $.ajaxSettings.beforeSend(xhr, settings);
        },
        success: function (b) {
            console.log(b)
        },
        error: function (e) {
            toastr.warning('Failed to receive schema of indices, please try again later', '' );//+ e.responseText);
        }
    });
}