
/*
	This method retrives the all the chart types
*/
function getAllChartType(type)
{
	var res = ['Bullet Chart','CumulativeLine Chart','DiscreteBarChart','HistoricalBarChart','LineChart','LinePlusBar Chart','LineWithFocus Chart','MultiBar Chart',
	'MultiBarHorizontalChart','Multi Chart','OhlcBar Chart','PieChart','Scatter Chart','StackedAreaChart'];
	var res2 = ['Bar Chart','Line Chart','Horizontal BarChart','Pie Chart'];
	
	if(type == 'json'){
		
	}

	return res2;
}

/*
	This method retrives the all the options for chart in JSON Array
*/
function getChartOptions(chart_type)
{
	
	var donut = { key:'donut', default: 'false', type: 'boolean'};
	var height = { key:'height', default: '300', type: 'number'};
	var width = { key:'width', default: '800', type: 'number'};
	var showXAxis = { key:'showXAxis', default: 'true', type: 'boolean'};
	var showYAxis = { key:'showYAxis', default: 'true', type: 'boolean'};
	var showLegend = { key:'showLegend', default: 'false', type: 'boolean'};
	var isArea = { key:'isArea', default: 'false', type: 'boolean'};
	var donutRatio = { key:'donutRatio', default: '0.25', type: 'number'};
	var showLabels = { key:'showLabels', default: 'true', type: 'boolean'};
	var rightAlignYAxis = { key:'rightAlignYAxis', default: 'false', type: 'boolean'};
	var showValues = { key:'showValues', default: 'false', type: 'boolean'};
	var labelType = { key:'labelType', default: 'key', type: 'string'};
	var tooltips = { key:'tooltips', default: 'true', type: 'boolean'};
	
	var optionList = [];
	if(chart_type == 'Line Chart')
	{
		optionList.push(showXAxis);
		optionList.push(showYAxis);
		optionList.push(showLegend);
		optionList.push(isArea);
	} 
	else if(chart_type =='Pie Chart')
	{
		optionList.push(donut);
		optionList.push(donutRatio);
		optionList.push(showLegend);
		optionList.push(showLabels);
		optionList.push(labelType);
	}
	else if(chart_type =='Bar Chart')
	{
		optionList.push(showXAxis);
		optionList.push(showYAxis);
		optionList.push(tooltips);
		optionList.push(rightAlignYAxis);
		optionList.push(showValues);
		
		
	}else if(chart_type =='Horizontal BarChart'){
		optionList.push(showXAxis);
		optionList.push(showYAxis);
		optionList.push(showValues);
		optionList.push(showLegend);
		optionList.push(tooltips);
	}

	//Adding default options
	optionList.push(height);
	optionList.push(width);
	
	return optionList;
}

/*
	This method draw the chart 
*/
function drawChart(chartType, chartOptions, containerId, chartData)
{
	//d3.selectAll(containerId+" > *").remove();
	$(containerId).html("");
	
	var kangaColors = ["#1ab394",  "#79d2c0","#b3b3b3","#d3d3d3","#54cdb4"];
  d3.scale.kangaColors = function() {
      return d3.scale.ordinal().range(kangaColors);
  };
		    
	
	if(chartType == 'Line Chart')
	{

		nv.addGraph(function()
	    {
				var chart = nv.models.lineChart()
				            .x(function(d) { return d[0] })
				            .y(function(d) { return d[1] }) 
				            .color(d3.scale.category10().range())
				            .margin({left: 100})  //Adjust chart margins to give the x-axis some breathing room.
				            ;
				
				var opt = {};
				for(var i=0;i<chartOptions.length;i++)
				{
					var key = chartOptions[i].key;
					opt[key] = chartOptions[i].value;
				}
				
				chart.options(opt);
				console.log(opt);
				
				chart.xAxis
				  .axisLabel('Time')
				  .tickFormat(function(d) {
				      return d3.time.format('%H:%M:%S %p')(new Date(d))
				    });
				
				//chart.forceY([1,300]);
				//chart.yAxis
				//    .axisLabel('Values');
				//d3.selectAll(containerId+" > *").remove();
				d3.select(containerId)
				  .datum(chartData)
				  .call(chart);
				
				nv.utils.windowResize(chart.update);
				
				//return chart;
				});
	} 
	else if(chartType =='Pie Chart')
	{
		var c;
		nv.addGraph(function() 
		{
	  		var chart = nv.models.pieChart()
	      						.x(function(d) { return d.label })
	      						.y(function(d) { return d.value })
	      						.color(d3.scale.kangaColors().range())
	      						.showLabels(true);
	      						
	    
    
	    var opt = {};
			for(var i=0;i<chartOptions.length;i++)
			{
				var key = chartOptions[i].key;
				opt[key] = chartOptions[i].value;
			}
				
			chart.options(opt);
			console.log(opt);
			//d3.selectAll(containerId+" > *").remove();
			d3.select(containerId)
			  .datum(chartData)
			  .transition().duration(350)
			  .call(chart);
			nv.utils.windowResize(chart.update);
			
		});
		
	}else if(chartType =='Bar Chart')
	{
		nv.addGraph(function() 
		{
  		var chart = nv.models.discreteBarChart()
      .x(function(d) { return d.label })    //Specify the data accessors.
      .y(function(d) { return d.value })
      .staggerLabels(true)    //Too many bars and not enough room? Try staggering labels.
      ;
      var opt = {};
			for(var i=0;i<chartOptions.length;i++)
			{
				var key = chartOptions[i].key;
				opt[key] = chartOptions[i].value;
			}
				
			chart.options(opt);
			console.log(opt);
			d3.selectAll(containerId+" > *").remove();
			d3.select(containerId)
			  .datum(chartData)
			  .call(chart);
			nv.utils.windowResize(chart.update);
		});
		
		
	}else if(chartType =='Horizontal BarChart'){
		
		  nv.addGraph(function() 
		  {
		    var chart = nv.models.multiBarHorizontalChart()
		        .x(function(d) { return d.label })
		        .y(function(d) { return d.value })
		        .margin({top: 30, right: 20, bottom: 50, left: 175})
		        .showControls(false);        //Allow user to switch between "Grouped" and "Stacked" mode.
				
				var opt = {};
				for(var i=0;i<chartOptions.length;i++)
				{
					var key = chartOptions[i].key;
					opt[key] = chartOptions[i].value;
				}
					
				chart.options(opt);
				console.log(opt);
				
				chart.barColor(function (d, i) {
				    var colors = d3.scale.category20().range().slice(10);
				    return colors[i % colors.length-1];
				});

				//d3.selectAll(containerId+" > *").remove();
		    chart.yAxis
		        .tickFormat(d3.format(',.2f'));
		
		    d3.select(containerId)
		        .datum(chartData)
		        .call(chart);
		
		    nv.utils.windowResize(chart.update);
		
		    //return chart;
	});
	}else if(chartType =='Stack BarChart'){
		
		nv.addGraph(function()
    {
    	
		    
			 var chart = nv.models.multiBarChart()
											      .reduceXTicks(true)   
											      .rotateLabels(0)      
											      .showControls(true) 
											      .groupSpacing(0.1)    
											    ;
			
			//chart.color(["#FF0000","#00FF00","#0000FF"]);
			chart.barColor(["#FF0000","#00FF00","#0000FF"]);
			//chart.stacked(true); // default to stacked
  		//chart.showControls(false); 
  		
	    chart.yAxis.tickFormat(d3.format(',.1f'));
			//d3.selectAll(containerId+" > *").remove();
			d3.select(containerId)
			  .datum(chartData)
			  .call(chart);
			
			nv.utils.windowResize(chart.update);
			
			//return chart;
			});
	}
	else if(chartType =='Stacked Area Chart')
	{
		    
		var chart = nv.models.stackedAreaChart()
	                        .margin({right: 100})
	                        .x(function(d) { return d[0] })   
	                        .y(function(d) { return d[1] })  
	                        .useInteractiveGuideline(true)   
	                        .rightAlignYAxis(true)      
	                        .showControls(true)      
	                        .color(d3.scale.kangaColors().range())
	                        .clipEdge(true);
	
	          //Format x-axis labels with custom function.
     chart.xAxis
				  .axisLabel('Time')
				  .tickFormat(function(d) {
		      return d3.time.format('%H:%M:%S %p')(new Date(d))
		    });

      chart.yAxis
          .tickFormat(d3.format(',.2f'));

      d3.select(containerId)
        .datum(chartData)
        .call(chart);

      nv.utils.windowResize(chart.update);
	}

    
}

/*
	This method prepare the chart options for specific chart
*/

function prepareOptions(chartType)
{
		var options = $('[id^="chartOptionsId_"]');
	  var chartOptions = [];
	 
			if(chartType == 'Line Chart')
			{
				var boolean_options = ['clipEdge', 'showXAxis', 'showYAxis', 'showLegend', 'isArea'];
				chartOptions = iterateOptions(options, boolean_options);
			}
			else if(chartType =='Pie Chart')
			{
				var boolean_options = ['donut','showLegend','showLabels'];
			  chartOptions = iterateOptions(options, boolean_options);
			}
			else if(chartType =='Bar Chart')
			{
				var boolean_options = ['showXAxis', 'showYAxis','rightAlignYAxis','showValues','tooltips'];
			  chartOptions = iterateOptions(options, boolean_options);
			}
			else if(chartType =='Horizontal BarChart')
			{
				var boolean_options = ['showXAxis', 'showYAxis','showValues','tooltips','showLegend'];
			  chartOptions = iterateOptions(options, boolean_options);
			}
		console.log(chartOptions);
	  return chartOptions;
}

/*
	This is private method to iterete the chart options
*/

function iterateOptions(options, boolean_options)
{
		var chartOptions = [];

		$.each(options, function (index, value) 
	  {
	  	 try {
		      var opt = {};
		      var key = (options[index].id).split('_')[1];
		      opt["key"] =key;
		      
		      if(boolean_options.indexOf(key) >= 0){
		      	opt["value"] = eval( $("#"+options[index].id).val() );
		      }else{
		      	opt["value"] = $("#"+options[index].id).val();
		      }
	   	}
			catch(err) {
			    alert('Please Enter Correct Value.'+err.message);
			    return false;
			}
	    chartOptions.push(opt);
	  });
	  return chartOptions;
}

/*
	This is method prepare the field data
*/
function parseFields(json_data){
	var columns = json_data.cols;
	var colums_array = [];
	for(var i=0;i<columns.length;i++){
		var colums_json = {};
		colums_json['label'] = columns[i].label;
		colums_json['type'] = columns[i].type;
		colums_json['id'] = i;
		colums_array.push(colums_json);
	}
	return colums_array;
}

/*
	This is method use to prepare the data for chart on runtime based on chart type
*/
function parpareData(chart_type, chart_data, dim1, dim2)
{
	if(chart_type =='Bar Chart' || chart_type =='Horizontal BarChart' )
	{
		var data = [
			{
			"key": dim1,
			"values": []
			}
		];
		
		var data_array = [];
		for(var j=0;j<chart_data.rows.length;j++){
			var d = {};
			d['label'] = chart_data.rows[j].c[dim1].v;
			d['value'] = checkType(chart_data.rows[j].c[dim2].v);
			data_array.push(d);
		}
		
		data[0].values = data_array;
		return data;
	}	
	else if(chart_type =='Pie Chart')
	{
		var data = [];
		for(var j=0;j<chart_data.rows.length;j++)
		{
			var d = {};
			d['label'] = chart_data.rows[j].c[dim1].v;
			d['value'] = checkType(chart_data.rows[j].c[dim2].v);
			data.push(d);
		}
		return data;
	}
	else if(chart_type =='Line Chart' || chart_type =='Area Chart')
	{
		var data = [
			{
			"key": dim1,
			"values": []
			}
		];
		var data_array = [];
		for(var j=0;j<chart_data.rows.length;j++){
			data_array.push( [chart_data.rows[j].c[dim1].v,checkType(chart_data.rows[j].c[dim2].v)]);
		}
		data[0].values = data_array;
		return data;
		
	}else if(chart_type =='Stack BarChart')
	{
		
		var data = [];
		for(var j=0;j<chart_data.rows.length;j++){
			var d = {};
			d['key'] = "men";
			var values = [];
	
			for(var k=1;k<chart_data.rows[j].c.length;k++){
				//values.push(chart_data.rows[j].c[k].v);
				var v = {};
				v['x'] = chart_data.rows[j].c[0].v;
				v['y'] = chart_data.rows[j].c[k].v;
				//v['series'] = k;
				values.push(v);
			}
			d['values'] = values;
			data.push(d);
			
		}
		return data;
	}
}

/*
	This is private method to check the data type
*/
function checkType(value){
	
	if(typeof value === 'string' || typeof value === "boolean"){
				value = 1;
	}
	return value; 
}
