// This is going to bind the events ajaxStart and ajaxStop into the
// global ajax progress animation on the left of the topbar navigation
$(document).ready(function() {
	$('#progressbar').progressbar();
	$('#topbar').dropdown();

	$('#modal-paste-url').modal({
	    keyboard: true, show:false
    });
});

// Sets the value of the progress bar
function set_progress_bar_value(prog_value)
{
	$('#progressbar').progressbar({value: prog_value});
}

// Request packages list and return paste url
function paste_pkgs()
{
	$.ajaxQueue({
		url: '/paste_pkgs',
		dataType: 'json',
		cache: false,
		success: function(data){
			if(data.error != true) {
				$('#modal-paste-url #paste-url').val(data.result)
				$('#modal-paste-url').modal('show');
			} 			
		}
	})
}