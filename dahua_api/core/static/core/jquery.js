// table search function
// Light Javascript Table Filter
// -by Chris Coyier
(function(document) {

	'use strict';
	var LightTableFilter = (function(Arr) {
		var _input;
		function _onInputEvent(e) {
			_input = e.target;
			var tables = document.getElementsByClassName(_input.getAttribute('data-table'));
			Arr.forEach.call(tables, function(table) {
				Arr.forEach.call(table.tBodies, function(tbody) {
					Arr.forEach.call(tbody.rows, _filter);
				});
			});
		}
		function _filter(row) {
			var text = row.textContent.toLowerCase(), val = _input.value.toLowerCase();
			row.style.display = text.indexOf(val) === -1 ? 'none' : 'table-row';
		}
		return {
			init: function() {
				var inputs = document.getElementsByClassName('table-filter');
				Arr.forEach.call(inputs, function(input) {
					input.oninput = _onInputEvent;
				});
			}
		};
	})(Array.prototype);

	document.addEventListener('readystatechange', function() {
		if (document.readyState === 'complete') {
			LightTableFilter.init();
		}
	});
})(document);


// $(document).ready(function(){
//     $('#myTable').dataTable();
//   });

 $(document).ready(function(){
   $('#sitios-remotos-table').dataTable();
 });
 $(document).ready(function(){
   $('#sitios-local-table').dataTable();
 });

 $(document).ready(function(){
	$(".config").hide();

	$('.show-hide-config').on("click", function(){
		if ($(".config").is(":visible")){
			$(".config").hide();
			$(".show-hide-config").text("Show")
		}else{
			$(".config").show();
			$(".show-hide-config").text("Hide")
		}
	});
  });


  $(document).ready(function(){
	$('.show-hide-configB').on("click", function(){
		if ($(".configB").is(":visible")){
			$(".configB").hide();
			$(".show-hide-configB").text("Show")
		}else{
			$(".configB").show();
			$(".show-hide-configB").text("Hide")
		}
	});
  });

 

  $(document).on("click", "#checkbox-time", function() {
	if ($('#checkbox-time').is(':checked')) {
		$( ".input-current" ).prop( "disabled", true );
	}
	else{
		$( ".input-current" ).prop( "disabled", false );
	}
});



$(document).on("click", "#checkbox-all", function() {

    $('.checkbox-f').prop('checked', this.checked);
});




$(document).ready(function(){

	//hides dropdown content
	$(".size_chart").hide();
	
	//unhides first option content
	$("#0").show();
	
	//listen to dropdown for change
	$("#size_select").change(function(){
	  //rehide content on change
	  $('.size_chart').hide();
	  //unhides current item
	  $('#'+$(this).val()).show();
	});
	
  });



