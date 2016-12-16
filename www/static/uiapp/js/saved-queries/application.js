/**
 * Created by SRIN on 3/5/2015.
 */

/* Formatting function for row details - modify as you need */
function rowDetailFormat(d) {
    return '<table cellpadding="5" cellspacing="0" border="0" style="padding-left:50px;">' +
        '<tr>' +
        '<td>Query ID:</td>' +
        '<td>' + d.id + '</td>' +
        '</tr>' +
        '<tr>' +
        '<td>Query Name:</td>' +
        '<td>' + d.name + '</td>' +
        '</tr>' +
        '<tr>' +
        '<td>Updated:</td>' +
        '<td>' + d.updated + '</td>' +
        '</tr>' +
        '</table>';
}

$(document).ready(function () {
    // TOASTR INITIALIZATION
    toastr.options = {
        closeButton: true,
        progressBar: true,
        showMethod: 'slideDown',
        positionClass: "toast-top-center",
        timeOut: 4000
    };

    var table = $('#tbl-saved-queries').DataTable({
        "ajax": HOST + "/workspace/list",
        "columns": [
            {
                "className": 'details-control',
                "orderable": false,
                "data": null,
                "defaultContent": ''
            },
            {
                "data": "name",
                "orderable": true
            },
            {
                "data": "created",
                "orderable": true
            },
            {
                "data": "updated",
                "orderable": true
            },
            {"data": "owner"},
            {
                "data": null,
                "orderable": false
            }
        ],
        "order": [[1, 'asc']],
        "createdRow": function (row, data, index) {
            $('td', row).eq(1).html('<a href="' + HOST + '/workspace/?wfid=' + data.id + '">' + data.name + '</a>');
            $('td', row).eq(5).html('<a href="#" data_id="'+data.id+'" ><i class="fa fa-trash-o text-navy"></i></a>');

        }
    });

    // DELETE ROW BUTTON CLICKED
    $('#tbl-saved-queries tbody').on('click', 'td a i.fa-trash-o', function () {
        if (confirm('delete row?')) {
            //sent request to delete order with given id
            var table = $('#tbl-saved-queries').dataTable();
            var tr = $(this).closest('tr');
            var a = $(this).closest('a');
            var dataID = a.attr("data_id");
            var row = tr.get(0);
            $.ajax({
                type: 'POST',
                url: HOST + '/workspace/removequery/',
                data: {
                    id: dataID
                },
                "beforeSend": function(xhr, settings) {
                    console.log("Before Send");
                    $.ajaxSettings.beforeSend(xhr, settings);
                },
                success: function (b) {
                    if (b) {
                        table.fnDeleteRow(table.fnGetPosition(row));
                        toastr.success('Row Deleted', '');
                    }
                },
                error: function (e) {
                    toastr.warning('Failed to delete, please try again later', '');// + e.responseText);
                }
            });
        }
        return false;
    });

    // Add event listener for opening and closing details
    $('#tbl-saved-queries tbody').on('click', 'td.details-control', function () {
        var tr = $(this).closest('tr');
        var row = table.row(tr);
        if (row.child.isShown()) {
            // This row is already open - close it
            row.child.hide();
            tr.removeClass('shown');
        }
        else {
            // Open this row
            row.child(rowDetailFormat(row.data())).show();
            tr.addClass('shown');
        }
    });
});

