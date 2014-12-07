$(document).ready(function() {
    var RESYNC_SECONDS = 15;
    var secondsUntilNextResync;

    function syncTimes() {
	$.get('/api', function(times) {
	    console.log('resync');
	    $("#times").html('');
	    $(times).each(function(i,e) {
		$("#times").append('<div class="container"><span class="timer" data-seconds="'+e+'">'+secondsToDisplayTime(e)+'</div>');
	    });
	    reStyleContainers();
	    setTimeout(updateCounters, 1000);
	    //setTimeout(getTimes, 3000);
	    secondsUntilNextResync = RESYNC_SECONDS;
	});
    }

    function reStyleContainers() {
	var height = Math.floor(100 / $('div.container').length);
	$('div.container').css('height', height+'vh');
	$('div.container').css('line-height', height+'vh');
	
	$('div.container').each(function(i,e) {
	    var seconds = parseInt($(e).find('.timer').data('seconds'));
	    if(seconds < 180) {
		$(e).css('background-color', '#DB3026');
	    }

	    if(seconds >= 180 && seconds < 360) {
		$(e).css('background-color', '#7ABF66');
	    }

	    if(seconds > 360) {
		$(e).css('background-color', '#F9E14B');
	    }
	});
    }

    function updateCounters() {
	if(secondsUntilNextResync <= 0) {
	    syncTimes();
	    return;
	}
	
	$('.timer').each(function(i,e) {
	    var seconds = parseInt($(e).data('seconds'));
	    seconds--;
	    $(e).data('seconds', seconds);
	    $(e).html(secondsToDisplayTime(seconds));
	});

	reStyleContainers();	
	secondsUntilNextResync--;
	setTimeout(updateCounters, 1000);
    }
   
    function secondsToDisplayTime(seconds) {
	var minutes = Math.floor(seconds / 60);
	var seconds = seconds % 60;
	return padDigits(minutes)+':'+padDigits(seconds);
    }

    function padDigits(number) {
	return number <= 9 ? ("0"+number) : "" + number;
    }
    syncTimes();
});
