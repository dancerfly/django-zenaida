(function () {
	"use strict";

	var $,
		FORMDATA_SUPPORT = 'FormData' in window
		zf_hints = window.zf_hints = {};

	if ('jQuery' in window && typeof jQuery !== "undefined") {
		$ = jQuery;
	} else {
		if ('console' in window) console.warn("Zenaida hints AJAX does not work without jQuery. Please include jQuery on your page or write your own javascript to make AJAX calls.");
	}

	$(function () {
		$('[data-dismiss-hint]').on('submit.hintAjax', function (e) {
			var $form = $(this),
				formData = $form.serialize(),
				hideSelector = $form.data('dismiss-hint'),
				transition = $form.data('transition') || "fadeOut",
				transitionSpeed = $form.data('transition-speed') || 200,
				$el = $(hideSelector);

			// Hide the hint immediately, assuming the ajax request will be successful.
			if (transition == "none" || transitionSpeed == 0) $el.hide()
			if (transition == "slideUp") $el.slideUp(transitionSpeed);
			if (transition == "fadeOut") $el.fadeOut(transitionSpeed);

			// Fire an Ajax request to hide the hint on the database side.
			$.ajax({
				type: $form.attr('method'),
				url: $form.attr('action'),
				data: formData,
				dataType: 'json',
				error: function (data) {
					// We didn't actually successfully hide it! Put it back!
					$el.stop(); // in case it's still transitioning.
					$el.show();
					alert("Something went wrong. Please report this error to a site administrator.");
				}
			});

			// Prevent the form from actually submitting.
			e.preventDefault();
		});
	});
}());
