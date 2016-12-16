/*datatable initialization*/
var table = $('#device_list').DataTable({
    ajax: {
        "type" : "POST",
        "url": device_list_url,
        "error": handleAjaxError
    },
    columns: [
        {"data": "ip"},
        {"data": "device type"},
        {"data": "hostname"}
    ],
    order: [[ 1, "desc" ]],
    language: {
        "search": "Search: ",
        "emptyTable": "No data"
    }
});
