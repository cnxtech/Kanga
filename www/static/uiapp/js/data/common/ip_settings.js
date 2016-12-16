function bootbox_ip_settings(url,service_code) {
    bootbox.setDefaults("animate", true);
    bootbox.dialog({
        title: service_code+" connection - IP settings",
        message: '<div class="row">  ' +
            '<div class="col-md-12"> ' +
            '<form class="form-horizontal"> ' +
            '<div class="form-group"> ' +
            '<label class="col-md-3 control-label" for="name">IP Address</label> ' +
            '<div class="col-md-9"> ' +
            '<input id="bootbox-ip-address" name="ip_address" type="text" placeholder="127.0.0.1" class="form-control input-md"> ' +
            '<span class="help-block">Please provide an IP address</span> </div> ' +
            '</div> ' +
            '</div> </div>' +
            '</form> </div>  </div>',
        buttons: {
            success: {
                label: "Save",
                className: "btn-success",
                callback: function () {
                    var ip = $('#bootbox-ip-address').val();
                    url = url + '&ip_address='+ip
                    ajax_save_service_ip(url,service_code);
                }
            },
            cancel: {
                label: "Cancel",
                className: "btn-cancel"
            }
        }
    });

}

function ajax_save_service_ip(url,service_code){
    $.ajax({
        url: url,
        timeout: 3000,
        success: function(json) {
            bootbox_refresh(service_code, json.code, json.message);
        },
        error: function (xhr, ajaxOptions, thrownError) {
            alert(xhr.status);
            alert(thrownError);
            bootbox_refresh(xhr.status,thrownError);
        },
        complete: function(jqXHR) {
            console.log(jqXHR);
        },
        dataType:"json",
    });

}

function bootbox_refresh(service_code, return_code,return_message){
    bootbox.dialog({
        title: "Apply Now",
        message: '<div class="row">  ' +
            '<div class="col-md-12"> ' +
            '<h4>Click to Refresh button to retrieve the information from the given '+service_code+' service</h4><pre><i class="fa fa-info-circle"></i> '+
            return_code + ', '+return_message + '</pre>'+
            '</div>  </div>',
        buttons: {
            success: {
                label: "Refresh",
                className: "btn-success",
                callback: function () {
                    location.reload();
                }
            },
            cancel: {
                label: "Cancel",
                className: "btn-cancel"
            }
        }
    });
}