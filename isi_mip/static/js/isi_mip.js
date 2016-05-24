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
					// console.log($.trim(collinetext), $.trim(value));
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
			table.find('.widget-table-noentriesmessage td').hide();
		} else {
			table.find('.widget-table-noentriesmessage td').show();
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


		// Update links to download CSV or PDF with current filter
		$('a[data-tableid]').each(function() {
			var filternames = table.data('filternames');

			var param = "";
			$.each(filter, function(colnumber, value) {
				param += "&" + encodeURIComponent([filternames[colnumber]]) + "=" + encodeURIComponent(value);
			});

			if (searchvalue) {
				param += "&searchvalue=" + encodeURIComponent( searchvalue )
			}

			if (param) {
				// replace first & with ?
				param = param.replace('&','?');
			}

			var baseurl = $(this).attr('href');
			// Strip parameter
			if (baseurl.indexOf('?') > 0) {
				baseurl = baseurl.substring(0, baseurl.indexOf('?'));
			}

			$(this).attr('href', baseurl + param);
		});


		console.log('Table updated. activepage:',activepage,'filter:',filter,'rowsperpage:',rowsperpage,'rowsintable:',rowsintable,'numberofpages:',numberofpages, 'searchvalue:', searchvalue);

		$(window).trigger('colsreordered');

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
		var filternames = {}; // name attributes of filters

		$(this).find('select').each(function() {
			var selector = $(this);
			var colnumber = selector.data('colnumber');
			filternames[colnumber] = selector.attr('name');

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

		table.data('filternames', filternames);

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
		var containerChecked = selectfield.find('.widget-options-checked');
		var containerNotChecked = selectfield.find('.widget-options-notchecked');

		function sortItems() {
			// Put selected to top and unselected to bottom container
			// Eventually sort items alphabetically

			containerChecked.find('label').each(function() {
				// move unchecked items down
				if (!$(this).find('input').prop('checked')) {
					var item = $(this).detach();
					item.appendTo( containerNotChecked );
				}
			});

			containerNotChecked.find('label').each(function() {
				// move checked items up
				if ($(this).find('input').prop('checked')) {
					var item = $(this).detach();
					item.appendTo( containerChecked );
				}
			});
		}

		selectfield.on('change', 'input', function() {
			sortItems();
		});

		selectfield.find('.widget-select-customvalue').keypress(function (event) {
			var key = event.which;
			if(key == 13) { // the enter key code
				var value = $(this).val();

				// remove options that were manually entered before if this is a radio
				var singleselect = $(this).hasClass('widget-select-customvalue-singleselect');
				if (singleselect) {
					selectfield.find('.widget-select-newcustomvalue').remove();
				}

				// TODO: Make sure item is no duplicate

				// clone item template
				var newitem = $(selectfield.find('.widget-options-template').html());
				newitem
					.addClass('widget-select-newcustomvalue')
					.find('input')
					.prop('checked', true)
					.prop('value', value)
					.parent()
					.find('span').text(value);
				containerChecked.append(newitem);

				sortItems();

				// reset input
				$(this).val('');

				// Do not submit form
				event.preventDefault();
				return false;
			}
		});
	});
});

$(function() {
	$('.seeallblock').each(function() {
		var seeallblock = $(this);
		seeallblock.find('.widget-readmorelink').click(function (event) {
			event.preventDefault();
			seeallblock.find('.row .col-sm-3').show();
			$(this).remove();
		});
	});
});


$(function() {
	// Smooth scrolling to anchors
	// https://stackoverflow.com/questions/14804941
	$("a[href^='#']").on('click', function(e) {
		e.preventDefault();
		var hash = this.hash;
		$('html, body').stop().animate({
			scrollTop: $(this.hash).offset().top
		}, 600, function(){
			window.location.hash = hash;
		});
	});
});


$(function() {
	function alignrows() {
		// reset height of teasers
		$('.widget-page-teaser-magicgrow').css('min-height', 0);


		// Grow page teasers to row height
		$('.widget-page-teaser-magicgrow').each(function() {
			var pageTeaser = $(this);
			var row = pageTeaser.closest('.row');

			// Do nothing for XS
			if (pageTeaser.find('.widget-page-teaser-xs-detector').is(':visible')) {
				return;
			}

			var rowHeight = row.height();
			var col = row.find('> div').has(pageTeaser);
			var colHeight = col.height();
			var pageTeaserHeight = pageTeaser.outerHeight();


			// set min height
			pageTeaser.css('min-height', pageTeaserHeight + rowHeight - colHeight);
		});
	}

	$(window).on('resize load', function() {
		alignrows();
	});
	alignrows();
});



$(function() {
	function aligncols() {
		// Grow page teasers to row height
		$('.widget-table').each(function() {
			var table = $(this);
			var tableWidth = table.width();

			var firstRowCols = table.find('tbody > tr > td');

			// reset width of cols
			firstRowCols.css('width', 'auto');

			// force table cols to maximum of 50% table width
			firstRowCols.each(function() {
				if ($(this).width() > tableWidth * 0.5) {
					$(this).width(tableWidth * 0.5);
				}
			});
		});

		console.log('Table Colums set to max 50% width.');
	}

	$(window).on('resize colsreordered', function() {
		aligncols();
	});
	aligncols();
});

