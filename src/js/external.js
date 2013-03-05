$(document).ready(function() {
	console.log('test');

	$('#delete_link').on('click', function(){
		var answer = confirm("Do you really want to delete the project?")
		if (answer == false){
			return false;
		}
	});

	$( "#id_start_date" ).datepicker({ dateFormat: 'yy-mm-dd' }).val();
	$( "#id_end_date" ).datepicker({ dateFormat: 'yy-mm-dd' }).val();

	$('.errorlist').addClass('alert alert-error');

	$('.menu_option').on('click', function() {
		$(".menu_option").removeClass("active");
		$(this).addClass("active");
	});

	$(".menu_option").removeClass("active");

	var url = window.location.pathname;
	if (url == '/projects/') {
		$('#projects').addClass("active");
	}
	else if (url == '/projects/add') {
		$('#new_project').addClass("active");
	}
	else if (url == '/') {
		$('#home').addClass("active");	
	}
});