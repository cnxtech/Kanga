	var PAGESIZE = 16;
	var MAX_STRIKE_COUNT = 2;
	$.xhrPool = []; // array of uncompleted requests
	$.xhrPool.abortAll = function() { // our abort function
		$(this).each(function(idx, jqXHR) { 
			jqXHR.abort();
		});
		$.xhrPool.length = 0;
		callFinish();
	};

	function callFinish(){
		document.getElementById("Finished").innerHTML = "Finished Displaying Results";
	}
    function poll(i,strikeCount, url, outputTableName, result_topic) {
	var tableName = outputTableName
	console.debug("Entered inside poll")
	 $.ajax({url: url,
			 data:{result_topic:result_topic, pagesize:PAGESIZE},
			 timeout: 30000,
			 beforeSend: function(jqXHR) { // before jQuery send the request we will push it to our array
							$.xhrPool.push(jqXHR);
						},
                success: function(json) {
						page = json["data"];
						fields = json["fields"];
						if(page.length > 0){
							if(i == 0)
								drawFields(tableName, fields);
							drawTable(tableName, page, fields);
						}
						if(page.length == 0)
							strikeCount = strikeCount + 1;
						if(strikeCount < MAX_STRIKE_COUNT)
							poll(i+page.length, strikeCount, url, outputTableName, result_topic);
						else
							callFinish();
						console.log("leaving success function ... " + Date())
			},
			error: function (xhr, ajaxOptions, thrownError) {
						alert(xhr.status);
						alert(thrownError);
					},
			complete: function(jqXHR) { // when some of the requests completed it will splice from the array
						var index = $.xhrPool.indexOf(jqXHR);
						if (index > -1) {
							$.xhrPool.splice(index, 1);
						}
					},
			dataType:"json",
		}
		);
		console.log("after ajax ....." + Date());
	}
	function drawFields(tableName, fields){
		var row = $("<tr />")
		$(tableName).append(row); //this will append tr element to table... keep its reference for a while since we will add cels into it
		for (var i = 0; i < fields.length; i++) {
			row.append($("<th>" + fields[i] + "</th>"));
		}
	}
	function drawTable(tableName,data,fields) {
		for (var i = 0; i < data.length; i++) {
			drawRow(tableName,data[i],fields);
		}
	}

	function drawRow(tableName, rowData, fields) {
		var row = $("<tr />")
		$(tableName).append(row); //this will append tr element to table... keep its reference for a while since we will add cels into it
		for (var i = 0; i < fields.length; i++) {
			row.append($("<td>" + rowData[fields[i]] + "</td>"));
		}
	}