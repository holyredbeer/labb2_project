$(document).ready(function() {
	console.log('test');

	$('#delete_link').on('click', function(){
		var answer = confirm("Do you really want to delete the project?")
		if (answer == false){
			return false;
		}
	});
});