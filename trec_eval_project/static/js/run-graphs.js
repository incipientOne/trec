google.charts.load('current', {'packages':['corechart']});


google.charts.setOnLoadCallback(drawRecallChart);
google.charts.setOnLoadCallback(drawPNChart);
google.charts.setOnLoadCallback(drawBasic);

function drawRecallChart() {
	if(typeof data_recall != 'undefined'){
		var data = google.visualization.arrayToDataTable(data_recall);

		var options = options_recall;

		var chart = new google.visualization.ScatterChart(document.getElementById('recall_chart_div'));
		chart.draw(data, options);
	}
}


function drawPNChart() {
	if(typeof data_pn != 'undefined'){
		var data = google.visualization.arrayToDataTable(data_pn);

		var options = options_pn;

		var chart = new google.visualization.ScatterChart(document.getElementById('pn_chart_div'));
		chart.draw(data, options);
	}
}

function drawBasic() {
	if(typeof data_basic != 'undefined'){
		var data = google.visualization.arrayToDataTable(data_basic);

		var options = options_basic;

		var chart = new google.visualization.BarChart(document.getElementById('chart_div'));

		chart.draw(data, options);
  	}
}