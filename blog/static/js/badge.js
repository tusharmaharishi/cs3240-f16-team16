$(document).ready(function(){
	$.ajax("/get_unread_messages", {
		method: 'GET',
		success: function(response){
			console.log(response);
			$('#unread_messages').text(response);
		}
	});
});