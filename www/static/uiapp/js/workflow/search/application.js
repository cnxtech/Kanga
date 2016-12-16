
    //This method suppress the datatable warnings
    function supressDataTableWarning()
    {
        var nativeAlert = window.alert;
        window.alert = (function()
        {
            return function(message)
            {
                if(message.indexOf("DataTables warning") === 0){
                    console.warn(message)
                }else{
                    nativeAlert(message);
                }
            }
        })();
    }

    function handleAjaxError( xhr, textStatus, error ) {
        if ( textStatus === 'timeout' ) {
            alert( 'The server took too long to send the data.' );
        }
        else {
            alert( 'An error occurred on the server. Please try again in a minute.' );
        }
    }

    function toggleTab(TabIndex) {
        $('#tab-'+TabIndex+'-li').addClass('active');
        $('#tab-'+TabIndex+'-link').attr('aria-expanded',true);
        $('#tab-'+TabIndex).addClass('tab-pane active');

        for(var i = 1; i<7; i++){
            if(i == TabIndex){

            }else{
                $('#tab-'+i+'-li').removeClass('active');
                $('#tab-'+i+'-link').removeClass('active');
                $('#tab-'+i+'-link').attr('aria-expanded',false);
                $('#tab-'+i).attr('class','tab-pane');
                $('#tab-'+i).addClass('tab-pane');
            }
        }
    }

    //This method remove the variables in the variable panel
    function remove_var(searchTxtId, oldValue){
        if(typeof oldValue === 'undefined'){

        }else{
            var index_Var = oldValue.indexOf('$');
            if(index_Var == 0){
                console.log('removing.....');
                remove_variable(searchTxtId, oldValue);
            }
        }
    }

    //This method remove the variables in the variable panel
    function remove_variable(searchTxtId, oldValue){
        if(oldValue in var_map){
            var index = var_map[oldValue].indexOf(searchTxtId);
            var_map[oldValue].splice(index, 1);
            console.log('removing....');
            if(var_map[oldValue].length == 0){
                delete var_map[oldValue];

                var var_name = oldValue.substring(1, oldValue.length);
                var panel_id = var_name + '_panel';
                var dash_id = var_name + '_dash';
                $('#'+panel_id).remove();
                $('#'+dash_id).remove();
            }
        }
        console.log(var_map);
    }

    //This method use for setting the datetime settings for Datatime Picker
    function datetimeSetting(from, to){

            $('#'+from).datetimepicker({
                format: 'YYYY-MM-DDTHH:MM:ss'
            });
            $('#'+to).datetimepicker({
                format: 'YYYY-MM-DDTHH:MM:ss'
            });

            $('#'+from).on("dp.change", function (e) {
                $('#'+to).data("DateTimePicker").minDate(e.date);
            });
            $('#'+to).on("dp.change", function (e) {
                $('#'+from).data("DateTimePicker").maxDate(e.date);
            });
    }

    //This method is use in Edit flow
    function init_varPanel(var_json) {

        var keysbyindex = Object.keys(var_json);
        for(var i = 0;i<keysbyindex.length;i++){
            var var_name = keysbyindex[i];
            var panel_id = var_name + '_panel';
            var dash_id = var_name + '_dash';
            var html = '<div class="form-group" id="'+panel_id+'">'+
                        '<label class="col-lg-1 control-label">'+var_name+'</label>'+
                        '<div class="col-lg-2">'+
                        '    <input name="$'+keysbyindex[i]+'" class="form-control" type="text" value="'+var_json[keysbyindex[i]]+'">'+
                        '</div></div><div class="hr-line-dashed" id="'+dash_id+'"></div>';

            $('#variablesDiv').append(html);
            var txtList = [];
            var_map['$'+var_name] = txtList;
        }
        console.log(var_map);
    }

    //This method add the variables in the variable panel
    function add_variable(searchTxtId, selectedSearchTxt, field ) {
        if(typeof selectedSearchTxt === 'undefined'){
            return;
        }
        var index_Var = selectedSearchTxt.indexOf('$');
        var var_name = selectedSearchTxt.substring(1, selectedSearchTxt.length);
        var var_id = selectedSearchTxt;
        if(index_Var == 0 && field != 'match_all' )
        {
             if(var_id in var_map){

                if(var_map[var_id].indexOf(searchTxtId) == -1 ){
                    var_map[var_id].push(searchTxtId);
                }
             }else{
                var txtList = [];
                txtList.push(searchTxtId);
                var_map[var_id] = txtList;
                var panel_id = var_name + '_panel';
                var dash_id = var_name + '_dash';

                var html = '<div class="form-group" id="'+panel_id+'">'+
                            '<label class="col-lg-1 control-label">'+var_name+'</label>'+
                            '<div class="col-lg-2">'+
                            '    <input name="'+var_id+'" class="form-control" type="text" value="0">'+
                            '</div></div><div class="hr-line-dashed" id="'+dash_id+'"></div>';

                $('#variablesDiv').append(html);
                toastr.success('Variable has been added in the Variables Panel Successfully!', '');
                toggleTab(4);
             }
              console.log(var_map);
        }
    }

    function prepare_varJson() {
        var out = {};
        var keysbyindex = Object.keys(var_map);
        for(var i=0;i<keysbyindex.length;i++){
            var k = keysbyindex[i];
            var txt_k = k.substring(1, k.length);
            var v = $('input[name="'+k+'"]').val();
            out[txt_k] = v;
        }
        console.log(out);
        return JSON.stringify(out);
    }

    // This method use to remove the search panel
    function removeme( panel, dash, panelType, searchTxtId, rangeTxtId1, rangeTxtId2)
    {
        var index_Var = $('#'+searchTxtId).val().indexOf('$');
        if(index_Var == 0){
            remove_variable(searchTxtId, $('#'+searchTxtId).val());
        }

        index_Var = $('#'+rangeTxtId1).val().indexOf('$');
        if(index_Var == 0){
            remove_variable(rangeTxtId1, $('#'+rangeTxtId1).val());
        }

        index_Var = $('#'+rangeTxtId2).val().indexOf('$');
        if(index_Var == 0){
            remove_variable(rangeTxtId2, $('#'+rangeTxtId2).val());
        }

        $('#'+dash).remove();
        $('#'+panel).remove();
        if(panelType == 'searchPanel'){
            count--;
        }else{
            sortCount--;
        }
    }

    function removeme_sortPanel( panel, dash){
        $('#'+dash).remove();
        $('#'+panel).remove();
        sortCount--;
    }

    function removeme_groupByPanel( panel, dash){
        $('#'+dash).remove();
        $('#'+panel).remove();
        groupByCount--;
    }

    //This will set the global timefield if Query contains timerange
    function fillTimeField(tag, search_query)
    {
        if(search_query.length>0 && tag == 'must')
        {
            var query = search_query[0];
            var keysbyindex = Object.keys(query);

            if(keysbyindex[0] == 'range'){
              var doc=query[keysbyindex[0]];
              var doc_key = Object.keys(doc);
              var value = doc[doc_key[0]];
              var from =  value[Object.keys(value)[0]];
              var to =  value[Object.keys(value)[1]];
              if(timeFields.indexOf(doc_key[0]) >= 0 ){
                  $('#date_from').val(from);
                  $('#date_to').val(to);
              }else{
                return 0;
              }
              return 1;
          }
        }
        return 0;
    }

    function add_var_JSON(searchTxtId, value)
    {
        if(value.indexOf('$') == 0){
            if(value in var_map){

                if(var_map[value].indexOf(searchTxtId) == -1 ){
                    var_map[value].push(searchTxtId);
                }
             }else{
                var txtList = [];
                txtList.push(searchTxtId);
                var_map[value] = txtList;
            }

        }
        console.log(var_map);

    }

    //This method formulate the JSON Query
    function prepareJsonSearch(action)
    {
        var l = $('div[id*="searchPanel"]').length;
        var s = $('select[id*="sortBy_"]').length;
        var g = $('select[id*="groupBy_"]').length;
        aggTableColumns = [];

        var from = $('#from').val();
        var to = $('#to').val();
        var sortBy = [];

        //Adding the first options of sort in query
        if($('#sortBy').val() == 'None'){

        }else{
            var opt = {};
            opt[$('#sortBy').val()] = $('#order').val();
            sortBy.push(opt);
        }

        //Interate all sort options for query based on dynamic panel
        for(var i = 0; i<s ; i++){
            var sort_By = $('select[id*="sortBy_"]')[i].id;
            if($('#'+sort_By).val() != 'None'){
                var order = $('select[id*="order_"]')[i].id;
                var opt = {};
                opt[$('#'+sort_By).val()] = $('#'+order).val();
                sortBy.push(opt);
            }
        }
        var groupCount = 0;
        //Integrate all group by options for query based on dynamic panel
        var aggOn = $('#aggOn').val();
        var aggFunction = $('#aggFunction').val();
        if(aggOn != 'None' && $('#groupBy_0').val() != 'None')
        {
            for(var i = (g-1); i>=0 ; i--)
            {
                var groupByValue = $("#groupBy_"+i).val();
                var groupByString = groupByValue+'_';

                //Validation check
                if(groupByValue != 'None') {
                    if(groupCount == 0) {
                            var opt = {
                                     groupByString:
                                      {
                                          "terms": {
                                            "field": groupByValue
                                          },
                                            "aggs" : {
                                                "aggregationOn" : {}
                                            }
                                      }
                                    };

                            opt.groupByString.aggs.aggregationOn[aggFunction.toString()] = {"field" : aggOn}

                            //Adding the aggregation on query json
                            groupByJson = opt;
                            groupCount++;

                            //Adding the column for aggregation
                            var agg_column = {};
                            agg_column['data'] =groupByValue;
                            agg_column['name'] =groupByValue;
                            aggTableColumns.push(agg_column);
                            agg_column = {};
                            agg_column['data'] ='value';
                            agg_column['name'] =aggFunction.toString()+'('+aggOn+')';
                            aggTableColumns.push(agg_column);

                        } else {

                            //This is top level aggregation based on multigroup by scenario
                            var opt = {
                                     groupByString:
                                      {
                                          "terms": {
                                            "field": groupByValue
                                          }
                                      }
                                    };
                             opt.groupByString["aggs"] = groupByJson;
                             groupByJson = opt;

                             var agg_column = {};
                             agg_column['data'] =groupByValue;
                             agg_column['name'] =groupByValue;
                             aggTableColumns.push(agg_column);
                        }
                    }
            }
        }

        var query = {"query":{"bool":{"must":[],"must_not":[],"should":[]}},"from": from,"size": to,"sort":sortBy,"facets":{}};

        //Adding group by in it's selected
        if(groupCount>0) query["aggs"] = groupByJson;

        //Adding the global Time Search in the query
        if($('#date_from').val() != '' && $('#date_to').val()){
            var json1 = {};
            var json2={};
            json2['from'] = $('#date_from').val();
            json2['to'] = $('#date_to').val();
            json1[$('#time_field').val()] = json2;
            query.query.bool.must.push({ 'range' : json1});
        }

        //Finding the list of search panel and interate over loop
        for(var i = 0; i<l ; i++)
        {
            //Preparing the IDs for retrive the elements
            var search_ = 'search_' + i;
            var searchDoc_ = 'searchDoc_' + i;
            var searchTerm_ = 'searchTerm_' + i;
            var searchTxt_ = 'searchTxt_' + i;

            //Retrives all Search items IDs and Values
            var search_val = $('#'+search_).val();
            var search_term = $('#'+searchTerm_).val();
            var search_doc = $('#'+searchDoc_).val();
            var search_txt = $('#'+searchTxt_).val();

            var index_Var = search_txt.indexOf('$');
            if(index_Var == 0 && action == 'test' ){
                search_txt = $('input[name="'+search_txt+'"]').val();
            }

            //Constructing Json Query
            var opt = ['term', 'wildcard','prefix', 'text'];
            var json1 = {};
            if(search_doc == 'match_all')
            {
                var json2 = {};
                json1['match_all'] = json2;
            }
            else if( opt.indexOf(search_term) >= 0 )
            {
                var json2 = {};
                json2[search_doc] = search_txt;
                json1[search_term] = json2;
            }else if(search_term == 'query_string'){
                var json2 = {};
                json2['default_field'] = search_doc;
                json2['query'] = search_txt;
                json1[search_term] = json2;
            }
            else if(search_term == 'missing'){
                var json2 = {
                    "filter": {
                        "missing": {}
                    }
                };
                json2.filter.missing['field'] = search_doc;
                json1['constant_score'] = json2;
            }
            else if(search_term == 'fuzzy'){
                var json2 = {};
                json2[search_doc] = { value : search_txt };
                json1[search_term] = json2;
            }
            else if(search_term == 'range'){
                var range_div_time_ = 'range_div_time_' + i;
                if($('#'+range_div_time_).is(':hidden'))
                {
                    var range_1 = 'range_'+i+'_1';
                    var range_2 = 'range_'+i+'_2';
                    var range_1_txt = 'range_'+i+'_1_txt';
                    var range_2_txt = 'range_'+i+'_2_txt';

                    //Retrives all Search items IDs and Values
                    var range_1_val = $('#'+range_1).val();
                    var range_2_val = $('#'+range_2).val();
                    var range_1_txt_val = $('#'+range_1_txt).val();
                    var range_2_txt_val = $('#'+range_2_txt).val();

                    var var_range_1_val = range_1_txt_val.indexOf('$');
                    if(var_range_1_val == 0 && action == 'test' ){
                        range_1_txt_val = $('input[name="'+range_1_txt_val+'"]').val();
                    }

                    var var_range_2_val = range_2_txt_val.indexOf('$');
                    if(var_range_2_val == 0 && action == 'test' ){
                        range_2_txt_val = $('input[name="'+range_2_txt_val+'"]').val();
                    }

                    var json2 = {};
                    var json3={};
                    json3[range_1_val] = range_1_txt_val;
                    json3[range_2_val] = range_2_txt_val;

                    json2[search_doc] = json3;
                    json1[search_term] = json2;
                }else{
                    var range1 = 'range_div_time_'+i+'_from';
                    var range2 = 'range_div_time_'+i+'_to';

                    var range1_val = $('#'+range1).val();
                    var range2_val = $('#'+range2).val();

                    var json2 = {};
                    var json3={};
                    json3['from'] = range1_val;
                    json3['to'] = range2_val;

                    json2[search_doc] = json3;
                    json1['range'] = json2;
                }
            }
            //Adding the Query element
            if(search_val == 'must')            query.query.bool.must.push(json1);
            else if(search_val == 'must_not')   query.query.bool.must_not.push(json1);
            else                                query.query.bool.should.push(json1);
        }

        $('#raw_query').val( JSON.stringify(query,null,'\t'));
    }

    // This method add the Toggle Button in the panel in Create/Edit mode
    function addColumns()
    {
        $('#toggleColumns').html('');
        toggle_column_map = [];
        var html = '<p>';
        console.log(toggle_column_edit_mode.length);

        // Check if there is any value in toggle column list. if not than ignore
        if(toggle_column_edit_mode.length > 0) {

            for (var i=0; i<tableColumns.length; i++)
            {
                var column = tableColumns[i]['data'];
                var index = toggle_column_edit_mode.indexOf(column);
                var style = 'btn btn-w-m btn-default btn-xs toggle-vis';
                if (index > -1) {
                    style = 'btn btn-w-m btn-primary btn-xs toggle-vis';
                    toggle_column_map.push(i);
                }
                if(column.toString().length>20) {
                    var temp = column.toString().substring(0,5) +'...'+column.toString().substring(column.toString().length-5,column.toString().length);
                    html += '<button type="button" class="'+style+'"  data-column="'+i+'" >'+temp+'</button>&nbsp;';
                } else {
                    html += '<button type="button" class="'+style+'"  data-column="'+i+'" >'+column.toString()+'</button>&nbsp;';
                }
            }

        } else {
            for (var i=0; i<tableColumns.length; i++)
            {
                var column = tableColumns[i]['data'];
                if(column.toString().length>20) {
                    var temp = column.toString().substring(0,5) +'...'+column.toString().substring(column.toString().length-5,column.toString().length);
                    html += '<button type="button" class="btn btn-w-m btn-primary btn-xs toggle-vis"  data-column="'+i+'" >'+temp+'</button>&nbsp;';
                } else {
                    html += '<button type="button" class="btn btn-w-m btn-primary btn-xs toggle-vis"  data-column="'+i+'" >'+column.toString()+'</button>&nbsp;';
                }
                toggle_column_map.push(i);
            }

        }

        if(toggle_flag) toggle_column_edit_mode = [];

        $('#toggleColumns').append(html+'</p>');

        // Register the click event
        $('button.toggle-vis').on( 'click', function (e)
        {
              var class_value = $(this).attr('class');
              var data_column = $(this).attr('data-column');
              var index = toggle_column_map.indexOf(parseInt(data_column));

              if(class_value == 'btn btn-w-m btn-primary btn-xs toggle-vis')
              {
                $(this).removeClass('btn btn-w-m btn-primary btn-xs toggle-vis');
                $(this).addClass('btn btn-w-m btn-default btn-xs toggle-vis');
                if (index > -1) {
                    toggle_column_map.splice(index, 1);
                }
              }else
              {
                $(this).removeClass('btn btn-w-m btn-default btn-xs toggle-vis');
                $(this).addClass('btn btn-w-m btn-primary btn-xs toggle-vis');
                toggle_column_map.push(parseInt(data_column));
              }
        });
    }

    function toggleTableColumn(table) {

        for(var i=0 ;i<tableColumns.length; i++) {
            if(toggle_column_map.indexOf(i) == -1 )
            {
                var column = table.column(i);
                column.visible(false);
            }
        }
    }

    function saveToggleColumn(){
        var save_column = new Array();
        for(var i=0 ;i<toggle_column_map.length; i++) {
            var column_meta = {};
            column_meta['index'] = i;
            column_meta['field'] = tableColumns[ toggle_column_map[i] ]['data'];
            save_column.push( tableColumns[ toggle_column_map[i] ]['data'].toString() );
        }
        console.log(save_column);

        return save_column;
    }

    $('#builder-query-name').on('click', function () {
        prepareJsonSearch('save');

        var raw_query = $('#raw_query').val();
        var index = $('#indexCombo1').val();
        var doc_type = $('#doc_field').val();
        var var_json = prepare_varJson();
        var selected_fields = saveToggleColumn();

        if(selected_fields.length == 0){
                alert('Please select at least 1 column');
                return;
        }

        // This is importent. getting the csrfmiddlewaretoken from parent html and passing to 'Save' ajax action call
        var csrfmiddlewaretoken = $("input[name=csrfmiddlewaretoken]").val();
        // Check for Edit Query or First time Save
        if($('#save-workflow').html() == 'Save')
        {
            var query_name = $('#builder-query-name').html();
            var queryDescription = $('#builder-query-description').html();

            bootbox.dialog({
            title: "Save Query - Choose Query Name!",
            message: '<div class="row">  ' +
                '<div class="col-md-12"> ' +
                '<form class="form-horizontal"> ' +
                '<div class="form-group"> ' +
                '<label class="col-md-3 control-label" for="name">Name</label> ' +
                '<div class="col-md-6"> ' +
                '<input id="bootbox-query-name" name="name" value="'+query_name+'" type="text" placeholder="New Query" class="form-control input-md"> ' +
                '<span class="help-block">Please choose a name</span> </div> ' +
                '</div> ' +
                '<div class="form-group"> ' +
                '<label class="col-md-3 control-label" for="description">Description</label> ' +
                '<div class="col-md-9"> ' +
                '<textarea id="bootbox-query-description" name="description" placeholder="This is new query" type="text" class="form-control input-md"> '+queryDescription+'</textarea> ' +
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

                        $.ajax({
                            type: 'POST',
                            url: url_queryupdate,
                            data: {
                                query_name: query_name,
                                updated_query_name: name,
                                description: description,
                                doc_type : doc_type,
                                query: raw_query,
                                index: index,
                                var_json : var_json,
                                selected_fields : selected_fields,
                                csrfmiddlewaretoken : csrfmiddlewaretoken
                            },
                            success: function (b) {
                                toastr.success('Workspace Query "'+name+'" has been update successfully!', '');
                                $('#builder-query-name').html(name);
                                $('#builder-query-description').html(description);
                                drawRecentQueryTable();
                            },
                            error: function (e) {
                                console.log(e)
                                toastr.warning('Failed to Update Query, please try again later', '' );
                            }
                        });
                       }
                    },
                    cancel: {
                        label: "Cancel",
                        className: "btn-cancel"
                    }
                }
            });
        }
        else
        {
            bootbox.dialog({
            title: "Save Query - Choose Query Name!",
            message: '<div class="row">  ' +
                '<div class="col-md-12"> ' +
                '<form class="form-horizontal"> ' +
                '<div class="form-group"> ' +
                '<label class="col-md-3 control-label" for="name">Name</label> ' +
                '<div class="col-md-6"> ' +
                '<input id="bootbox-query-name" name="name" type="text" placeholder="New Query" class="form-control input-md"> ' +
                '<span class="help-block">Please choose a name</span> </div> ' +
                '</div> ' +
                '<div class="form-group"> ' +
                '<label class="col-md-3 control-label" for="description">Description</label> ' +
                '<div class="col-md-9"> ' +
                '<textarea id="bootbox-query-description" name="description" placeholder="This is new query" type="text" class="form-control input-md"/> ' +
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
                        $.ajax({
                            type: 'POST',
                            url: url_querysave,
                            data: {
                                query_name: name,
                                description: description,
                                query: raw_query,
                                doc_type : doc_type,
                                index: index,
                                var_json : var_json,
                                selected_fields : selected_fields,
                                csrfmiddlewaretoken : csrfmiddlewaretoken
                            },
                            success: function (b) {
                                toastr.success('Workspace Query "'+name+'" has been saved successfully!', '');
                                $('#builder-query-name').html(b.query_name);
                                $('#builder-query-description').html(description);
                                $('#save-workflow').html('Save');
                                drawRecentQueryTable();
                            },
                            error: function (e) {
                                console.log(e)
                                toastr.warning('Failed to save query, please try again later', '' );
                            }
                        });
                       }
                    },
                    cancel: {
                        label: "Cancel",
                        className: "btn-cancel"
                    }
                }
            });
        }
       });

    $('#refresh_index').on('click', function () {
        $.ajax({
            type: 'GET',
            url: url_es_sync_index,
            success: function (b) {
                toastr.success('ES Index has been refreshed successfully!', '');
                window.location = window.location.href;
            },
            error: function (e) {
                console.log(e)
                toastr.warning('Failed to refresh Index, please try again later', '' );
            }
        });
    });

    //This method render the Aggregate Table
    function prepareAggregateTable(json_result)
    {

        $('#agg_query_result_ibox-content').html("");
        var header = '<table id="agg_query_result" class="table  table-hover  table-striped" width="100%"><thead><tr>';

        for (var i=0; i<aggTableColumns.length; i++)
        {
            var column = aggTableColumns[i]['name'];
            header += '<th>'+column.toString()+'</th>';
        }

        header +='</tr></thead><tbody></tbody></table>';
        $("#agg_query_result_ibox-content").append(header);

        $('#agg_query_result').DataTable( {
            "dom": 'T<"clear">lfrtip',
            "tableTools": {
            "aButtons": [{
                        "sExtends": "copy",
                        "sButtonText": "Copy to clipboard"
                    },
                    {
                        "sExtends": "csv",
                        "sButtonText": "Save to CSV"
                    },
                    {
                        "sExtends": "xls",
                        "sButtonText": "Save to Excel",
                    }],
                    "sSwfPath": "/static/uiapp/js/plugins/dataTables/swf/copy-csv-xls.swf"
            },
            "data": json_result,
            "columns":aggTableColumns
        });

    }

    //This method use in edit flow to prepare group by panel
    function iterateGroupBy(fields){

        if(fields.length>1){
            for(var i = 1; i<fields.length; i++){
                var groupByJson =fields[i];
                addGroupBy(groupByJson);
            }
        }
    }

    //This is utility method use in edit flow to prepare group by panel
    function findFields(query){
        var field = [];
        recFindField(query["aggs"], field);
        return field;
    }

    //This is utility method use in edit flow to prepare group by panel
    function recFindField(json, field)
    {
        if(typeof json["groupByString"] == 'undefined'){
       }else{
            field.push(json["groupByString"]["terms"]["field"]);
            recFindField(json["groupByString"]["aggs"],field)
       }
    }

    //This is utility method use in edit flow to prepare group by panel
    function findAggFunction(query){
        var field = [];
        recFindFunction(query["aggs"], field);
        return field;
    }

    //This is utility method use in edit flow to prepare group by panel
    function recFindFunction(json, field)
    {
        if(typeof json["groupByString"] == 'undefined'){
            var aggFunction = Object.keys(json["aggregationOn"]);
            field.push(aggFunction[0]);
            field.push(json["aggregationOn"][aggFunction[0]]["field"]);
       }else{
            recFindFunction(json["groupByString"]["aggs"],field)
       }
    }


