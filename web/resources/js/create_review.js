
$(document).ready(function() {
        $( "#slider" ).slider();
    
		$( "#overall_slider" ).slider({
			value:3,
			min: 1,
			max: 5,
			step: 1,
			slide: function( event, ui ) {
				$( "#overall_amount" ).val( "$" + ui.value );
			}
		});
		$( "#overall_amount" ).val( "$" + $( "#overall_slider" ).slider( "value" ) );

		$( "#pay_slider" ).slider({
			value:3,
			min: 1,
			max: 5,
			step: 1,
			slide: function( event, ui ) {
				$( "#pay_amount" ).val( "$" + ui.value );
			}
		});
		$( "#pay_amount" ).val( "$" + $( "#pay_slider" ).slider( "value" ) );
	
		$( "#hours_slider" ).slider({
			value:3,
			min: 1,
			max: 5,
			step: 1,
			slide: function( event, ui ) {
				$( "#hours_amount" ).val( "$" + ui.value );
			}
		});
		$( "#hours_amount" ).val( "$" + $( "#hours_slider" ).slider( "value" ) );

		$( "#diff_slider" ).slider({
			value:3,
			min: 1,
			max: 5,
			step: 1,
			slide: function( event, ui ) {
				$( "#diff_amount" ).val( "$" + ui.value );
			}
		});
		$( "#diff_amount" ).val( "$" + $( "#diff_slider" ).slider( "value" ) );
	});
