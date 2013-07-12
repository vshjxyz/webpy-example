// Defining a pseudo-enumeration
var ACT = {
	CONSOLE: '/consolelist',
	PRINT: '/printlist',
	WRITE: '/writelist',
	GET: '/getlist',
	EMAIL: '/emaillist',
	GIST: '/gistlist'
}

$(function() { 
	// Attaching all the click events to the callAjax method with different handlers and actions to cal
	$('#consolelist').click({action: ACT.CONSOLE, handler: consoleListHandler}, callAjax);
	$('#printlist').click({action: ACT.PRINT, handler: printListHandler}, callAjax);
	$('#writelist').click({action: ACT.WRITE, handler: writeListHandler}, callAjax);
	$('#emaillist').click({action: ACT.EMAIL, handler: emailListHandler}, callAjax);
	$('#gistlist').click({action: ACT.GIST, handler: gistListHandler}, callAjax);
	
	// Setting up the preloader to be hidden when no ajax actions are up
	$('#preloader')
    .hide()
    .ajaxStart(function() {
		$('.output').empty(); // Cleans the output DIV every time the loader is shown
        $(this).show();
    })
    .ajaxStop(function() {
        $(this).hide();
    });
});

// Method used to send ajax request to the web.py interface
function callAjax(e) {
	$.ajax({
		type: "GET",
  		url: e.data.action,
  		complete: e.data.handler
	});
	return false;
}

// Handling general errors with a message
function handleError() {
	$('.output').append('There was an error during the operation');
}

// Handler for the first button
function consoleListHandler(e, result) {
	if (result != 'success') {
		handleError();
		return;
	}
	$('.output').append('Check your python console!');
}

// Handler for the second button (printing directly the ordered list to the output DIV)
function printListHandler(e, result) {
	if (result != 'success') {
		handleError();
		return;
	}
	$('.output').append(e.responseText);
}

// Once the result is written to disk, it creates a link to download it 
function writeListHandler(e, result) {
	if (result != 'success') {
		handleError();
		return;
	}
	$('.output').append('File ' + e.responseText + ' created! Click <a href="' +
						ACT.GET +'/' + e.responseText +	'">here</a> to download it')
}

// After sending the email with the response, shows you where the email has been sent
function emailListHandler(e, result) {
	if (result != 'success') {
		handleError();
		return;
	}
	$('.output').append('E-mail (not really)sent to : ' + e.responseText);
}

// Using the result html_url from the python code to generate a direct link to the gist created
function gistListHandler(e, result) {
	if (result != 'success') {
		handleError();
		return;
	}
	$('.output').append('Gist created! click <a href="' + e.responseText + '">here</a> to see it');
}
