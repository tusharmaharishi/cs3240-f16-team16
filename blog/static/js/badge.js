$(document).ready(function(){
	$.ajax("/get_unread_messages", {
		method: 'GET',
		success: function(response){
			if(response != 0) {
				console.log(response);
				$('#unread_messages').text(response);
			} else {
				$('#unread_messages').text("");
			}
		}
	});
});