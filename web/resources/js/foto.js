$(document).ready(function() {
	$(".btn").button();  
	$('#username').change(function() {
		$('#uname').val($(this).val());
	});
});