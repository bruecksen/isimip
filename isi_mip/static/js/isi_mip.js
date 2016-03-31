$(function() {
	$('.widget-table').each(function() {
		var table = $(this);
		// number of pages this table has (0: no pagination)
		var pagecount = table.find('.widget-table-pagination').first().find('.widget-table-pagination-pagelink').length;


		table.find('.widget-table-showmore-button').click(function() {
			table.find('tbody tr').show();
			$(this).remove();
		});

		function showPage(pagenumber) {
			table.find('tbody tr[data-pagenumber='+ pagenumber +']').show();
			table.find('tbody tr:not([data-pagenumber='+ pagenumber +'])').hide();
			table.find('.widget-table-pagination-pagelink:not([data-pagenumber='+ pagenumber +'])').removeClass('widget-table-pagination-pagelink-active');
			table.find('.widget-table-pagination-pagelink[data-pagenumber='+ pagenumber +']').addClass('widget-table-pagination-pagelink-active');

			// Update links in prev next buttons:
			if (pagenumber == 1) {
				table.find('.widget-table-pagination-prevbutton').data('pagenumber', 1 ).addClass('disabled');
			} else {
				table.find('.widget-table-pagination-prevbutton').data('pagenumber', (pagenumber-1) ).removeClass('disabled');
			}
			if (pagenumber == pagecount) {
				table.find('.widget-table-pagination-nextbutton').data('pagenumber', pagenumber ).addClass('disabled');
			} else {
				table.find('.widget-table-pagination-nextbutton').data('pagenumber', (pagenumber+1) ).removeClass('disabled');
			}
		}

		// Init links
		table.find('.widget-table-pagination-prevbutton').data('pagenumber', 1).addClass('disabled');
		table.find('.widget-table-pagination-nextbutton').data('pagenumber', 2);
		if (pagecount < 2) { table.find('.widget-table-pagination-nextbutton').data('pagenumber', 1).addClass('disabled'); }

		// Click on page navigation
		table.find('.widget-table-pagination-pagelink, .widget-table-pagination-prevbutton, .widget-table-pagination-nextbutton').click(function() {
			var pagenumber = $(this).data('pagenumber');
			showPage(pagenumber);
		});

	});
});
