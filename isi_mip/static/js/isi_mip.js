$(function() {
	// Die Tabllen im widget-table haben spezielle Funktionen wie Paginierung, 

	function updateTable(table) {

		var activepage = table.data('activepage');
		var filter = table.data('filter');
		var rowsperpage = table.data('rowsperpage');
		var searchvalue = table.data('searchvalue');


		// set all rows to show and then apply filters, search and pagination
		table.find('tbody tr').addClass('widget-table-show');


		// disable rows by filter
		// iterate filters
		$.each(filter, function(colnumber, value) {
			// console.log('apply filer for colnumber', colnumber, 'and value', value);
			// iterate rows
			table.find('tbody tr').each(function() {
				// hide rows not matching filter
				var row = $(this);
				var showcolline = false;

				row.find('td:nth-child(' + colnumber + ')').find('.widget-table-col-line').each(function() {
					var colline = $(this);
					var collinetext = colline.text();
					console.log($.trim(collinetext), $.trim(value));
					if ( $.trim(collinetext) == $.trim(value) ) {
						showcolline = true;
					}
				});

				if (!showcolline) {
					row.removeClass('widget-table-show');
				}
			});
		});


		// disable rows by search string
		var searchwords = searchvalue.match(/\S+/g);
		if (searchwords) {
			// iterate rows
			table.find('tbody tr').each(function() {
				// hide rows not matching filter
				var row = $(this);
				var hit = true; // if all words are somewhere in the row

				// iterate search words
				$.each(searchwords, function(i, searchword) {
					var wordhit = false; // if this word is somewhere in the row
					searchword = searchword.toLowerCase();

					row.find('td').each(function() {
						// does any column contain the word?
						if ($(this).text().toLowerCase().indexOf(searchword) > -1) wordhit = true;
					});

					if (!wordhit) hit = false; // fail
				});

				if (!hit) row.removeClass('widget-table-show');
			});
		}


		// Pagination
		var rowsintable = table.find('tbody tr.widget-table-show').length; // rows in the table, all pages

		// show or hide message that no rows to show
		if (rowsintable) {
			$('.widget-table-noentriesmessage').hide();
		} else {
			$('.widget-table-noentriesmessage').show();
		}

		var numberofpages = Math.ceil(rowsintable / rowsperpage);
		// save back
		table.data('numberofpages', numberofpages);

		// hide rows in other pages
		table.find('tbody tr.widget-table-show').each(function(rownumber) {
			if ((rowsperpage * (activepage-1) > rownumber) || (rowsperpage * activepage <= rownumber)) {
				$(this).removeClass('widget-table-show');
			}
		});

		// show the pagination links needed
		table.find('.widget-pagination-pagelink').each(function() {
			if (($(this).data('pagenumber') > numberofpages) || (numberofpages < 2)) {
				$(this).hide();
			} else {
				$(this).show();
			}
		});


		table.find('tbody tr:not(.widget-table-show)').hide();
		table.find('tbody tr.widget-table-show').show().removeClass('widget-table-show');

		table.find('.widget-pagination-pagelink:not([data-pagenumber='+ activepage +'])').removeClass('widget-pagination-pagelink-active');
		table.find('.widget-pagination-pagelink[data-pagenumber='+ activepage +']').addClass('widget-pagination-pagelink-active');

		// Update status in prev next buttons:
		if (activepage == 1) {
			table.find('.widget-pagination-prevbutton').addClass('disabled');
		} else {
			table.find('.widget-pagination-prevbutton').removeClass('disabled');
		}
		if (activepage >= numberofpages) {
			// ( when numberofpages = 0 is activepage still 1 )
			table.find('.widget-pagination-nextbutton').addClass('disabled');
		} else {
			table.find('.widget-pagination-nextbutton').removeClass('disabled');
		}

		console.log('Table updated. activepage:',activepage,'filter:',filter,'rowsperpage:',rowsperpage,'rowsintable:',rowsintable,'numberofpages:',numberofpages, 'searchvalue:', searchvalue);

		// Update URL
		// TODO
	}



	$('.widget-table').each(function() {
		var table = $(this);

		// initialize table settings
		var filter = table.data('filter');
		if (!filter) table.data('filter', {});
		var activepage = table.data('activepage');
		if (!activepage) table.data('activepage', 1);
		var rowsperpage = table.data('rowsperpage');
		if (!rowsperpage) table.data('rowsperpage', 2000);
		var searchvalue = table.data('searchvalue');
		if (!searchvalue) table.data('searchvalue', '');


		table.find('.widget-table-showmore-button').click(function() {
			table.find('tbody tr').show();
			$(this).remove();
		});


		// Click on page navigation
		table.find('.widget-pagination-pagelink').click(function(event) {
			event.preventDefault();
			table.data('activepage', $(this).data('pagenumber'));
			updateTable(table);
		});
		table.find('.widget-pagination-prevbutton').click(function() {
			var activepage = table.data('activepage');
			if (activepage > 1) activepage--;

			table.data('activepage', activepage);
			updateTable(table);
		});
		table.find('.widget-pagination-nextbutton').click(function() {
			var activepage = table.data('activepage');
			var numberofpages = table.data('numberofpages');
			if (activepage < numberofpages) activepage++;
			// console.log('Button clicked. Now: activepage', activepage, 'numberofpages',numberofpages);

			table.data('activepage', activepage);
			updateTable(table);
		});

	});



	$('.widget-table-selector').each(function() {
		var table = $('#' + $(this).data('tableid'));
		var filter = table.data('filter');


		$(this).find('select').each(function() {
			var selector = $(this);
			var colnumber = selector.data('colnumber');

			selector.change(function() {
				// Show first page after filter change
				table.data('activepage', 1);

				var filtervalue = selector.val();
				if (filtervalue != 'tableselectordefaultall') {
					// set filter
					// console.log('set filter for col ', colnumber, ' filtervalue: ', filtervalue);
					filter[ "" + colnumber ] = filtervalue;
				} else {
					// unset filter
					// console.log('unset filter for col ', colnumber);
					delete filter[ "" + colnumber ];
				}

				updateTable(table);
			});
		});
		$(this).find('.widget-table-selector-search').on('keyup change paste input', function() {
			// Show first page after filter change
			table.data('activepage', 1);

			table.data('searchvalue', $(this).val());
			updateTable(table);
		});
	});
});



$(function() {
	$('.widget-expandable .widget-expandable-listitem-toggleable .widget-expandable-listitem-term').click(function() {
		$(this).closest('.widget-expandable-listitem').toggleClass('widget-expandable-listitem-term-open');
	});
});



$(function() {
	$('.widget-singleselect, .widget-multiselect').each(function() {
		var selectfield = $(this);

		selectfield.find('.widget-select-customvalue').keypress(function (event) {
			var key = event.which;
			if(key == 13) { // the enter key code
				var value = $(this).val();
				var optionselement = selectfield.find('.widget-options');
				var html = optionselement.find('label:last')[0].outerHTML;
				console.log(html);
				optionselement.append(html);
				optionselement.find('label:last')
					.prop('checked', true)
					.prop('value', value)
					.find('span').text(value);

				// reset input
				$(this).val('');
				// Do not submit form
				event.preventDefault();
				return false;
			}
		}); 
	});
});
