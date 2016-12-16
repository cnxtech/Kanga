/*datatable initialization*/
var table = $('#device_list').DataTable({
    ajax: {
        "type" : "POST",
        "url": connect_device_url,
        "error": handleAjaxError
    },
    columnDefs: [
        {
            targets: 0,
            orderable: false,
            searchable : false,
            className: "dt-center",
            render : function(data, type, full, meta){
                return '<input type="checkbox">';
            }
        }
    ],
    select : {
        style: 'multi',
        selector: 'td>input'
    },
    columns: [
        {"data": "select"},
        {"data": "ip"},
        {"data": "device type"},
        {"data": "hostname"}
    ],
    order: [[ 2, "desc" ]],
    language: {"search": "Search: "},
});

$('#device_list thead').on('click', '#selectAll', function(e){
    if($('td input[type="checkbox"]').length > $('td input[type="checkbox"]:checked').length){
        $('td input[type="checkbox"]:not(:checked)').trigger('click');
    }
    else{
        $('tbody tr td input').trigger('click');
    }
    e.stopPropagation();
});

$('#device_list tbody').on('click', 'input[type="checkbox"]', function(e){
    if($('td input[type="checkbox"]').length == $('td input[type="checkbox"]:checked').length){
        $('input#selectAll').prop('checked' , true);
    }
    else {
        $('input#selectAll').prop('checked' , false);
    }
    e.stopPropagation();
});

