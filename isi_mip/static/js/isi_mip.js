$(function() {
	// Die Tabllen im widget-table haben spezielle Funktionen wie Paginierung, 

	function updateTable(table) {

		var activepage = table.data('activepage');
		var filter = table.data('filter');
		var rowsperpage = table.data('rowsperpage');
		var searchvalue = table.data('searchvalue');


		// set all rows to show and then apply filters, search and pagination
		table.find('tbody tr').show();


		// disable rows by filter
		// iterate filters
		$.each(filter, function(colnumber, value) {
			// iterate rows
			table.find('tbody tr').each(function() {
				// hide rows not matching filter
				var row = $(this);
				var showcolline = false;

				row.find('td:nth-child(' + colnumber + ')').find('.widget-table-col-line').each(function() {
					var colline = $(this);
					var collinetext = colline.text();
					if ( $.trim(collinetext) == $.trim(value) ) {
						showcolline = true;
					}
				});

				if (!showcolline) {
					$(row).hide();
				}
			});
		});

		if (searchvalue) {
			var $rows = $('tbody tr');
			var val = '^(?=.*' + $.trim(searchvalue).split(/\s+/).join(')(?=.*') + ').*$',
				reg = RegExp(val, 'i'),
				text;
			console.log(val);
			$rows.show().filter(function() {
				text = $(this).text().replace(/\s+/g, ' ');
				return !reg.test(text);
			}).hide();
		}


		// Pagination
		var rowsintable = table.find('tbody tr:visible').length; // rows in the table, all pages

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
		table.find('tbody tr:visible').each(function(rownumber) {
			if ((rowsperpage * (activepage-1) > rownumber) || (rowsperpage * activepage <= rownumber)) {
				$(this).hide();
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


		// table.find('tbody tr:not(.widget-table-show)').hide();
		// table.find('tbody tr.widget-table-show').show().removeClass('widget-table-show');

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


		// console.log('Table updated. activepage:',activepage,'filter:',filter,'rowsperpage:',rowsperpage,'rowsintable:',rowsintable,'numberofpages:',numberofpages, 'searchvalue:', searchvalue);

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


		table.find('row:visible more-button').click(function() {
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

		$(this).find('.widget-table-selector-search').on('input', function() {
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


		if (selectfield.hasClass('widget-multiselect-nullable')) {
			// Radios are deselectable
			selectfield.on('click', '.widget-options-checked label', function(event) {
				// deselect this
				$(this).find('input').prop('checked', false);
				// Nicht gleich wieder aktivieren.
				event.preventDefault();
				// Vorsichtshalber nochmal sortieren.
				sortItems();
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
	$('.seeallblock .widget-readmorelink').click(function(event) {
		event.preventDefault();
		$(this).closest('.seeallblock').find('.col-sm-3').show();
		$(this).remove();
		$(window).trigger('resize');
	});
});


$(function() {
	// Smooth scrolling to anchors
	// https://stackoverflow.com/questions/14804941
	$("a.anchor-scroll").on('click', function(e) {
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
	setTimeout(alignrows, 500);
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

		// console.log('Table Colums set to max 50% width.');
	}

	$(window).on('resize colsreordered', function() {
		aligncols();
	});
	aligncols();
});



$(function() {
	$('abbr[data-original-title], abbr[title]').each(function() {
		var initiator = $(this);

		initiator.popover({
			'template': '<div class="popover" role="tooltip"><div class="arrow"></div><div class="popover-content"></div></div>',
			'content': initiator.attr('title'),
		});


		// http://stackoverflow.com/questions/32581987/need-click-twice-after-hide-a-shown-bootstrap-popover
		initiator.on('hidden.bs.popover', function (e) {
			$(e.target).data("bs.popover").inState = { click: false, hover: false, focus: false }
		});


		// Close popover on click outside initiating element
		$('body').click(function(e) {
			var target = $(e.target);
			if (!target.closest(initiator).length) {
				initiator.popover('hide');
			}

		});
	});
});



$(function() {
	// Paper editor


	Date.prototype.yyyymmdd = function() {
		var yyyy = this.getFullYear().toString();
		var mm = (this.getMonth()+1).toString(); // getMonth() is zero-based
		var dd  = this.getDate().toString();
		return yyyy +"-"+ (mm[1]?mm:"0"+mm[0]) +"-"+ (dd[1]?dd:"0"+dd[0]); // padding
	};


	$('.widget-paper-editor').each(function() {
		var paperEditor = $(this);


		function checkMaxPaperCount() {
			var maxPaperCount = paperEditor.data('maxpapercount');
			if (!maxPaperCount) return;

			var paperCount = paperEditor.find('.widget-paper-list .widget-paper-visualisation').length;

			// Show buttons for adding new papers only when allowed number of papers
			//  larger than actual number of papers.
			if (maxPaperCount <= paperCount) {
				paperEditor.find('.widget-paper-addbuttons').hide();
			} else {
				paperEditor.find('.widget-paper-addbuttons').show();
			}
		}

		function addPaper(title) {
			if (title) {
				var url = paperEditor.data('apibaseurl');
				// Same Origin mirror of this: http://api.crossref.org/works?rows=1&query=Yolo

				$.getJSON( url, {'query':title}, function( data ) {

					if (!data.message || !data.message.items || !data.message.items[0]) {
						console.log('No paper found!');
						paperEditor.find('.widget-paper-addbuttons-errormessage').show();
						return;
					}

					paperEditor.find('.widget-paper-addbuttons-errormessage').hide();
					console.log("Paper found:", data);
					var paper = data.message.items[0];


					var paperAuthor = '';
					if (paper.author) {
						// Iterate authors
						$.each(paper.author, function(index, author) {
							paperAuthor += author.family;

							if (author.given) {
								paperAuthor += ' '+author.given.charAt(0);
							}

							paperAuthor += ', ';
						});

						// Get rid of last ", "
						paperAuthor = paperAuthor.slice(0, -2);
					}

					if (paper.title) {
						var paperTitle = paper.title[0];
					} else {
						paperTitle = '';
					}

					if (paper['container-title']) {
						paperJournal = paper['container-title'][0];
					} else {
						paperJournal = '';
					}

					paperVolume = paper.volume;
					paperPage = paper.page;

					var paperDoi = paper.DOI;
					var paperUrl = paper.URL;

					if (paper.created && paper.created.timestamp) {
						var paperDate = new Date(paper.created.timestamp);
						var paperDate = paperDate.yyyymmdd();
					} else {
						paperDate = '';
					}

					// clone template
					var template = paperEditor.find('.widget-paper-visualisation-template').html();
					paperEditor.find('.widget-paper-list').append(template);

					// fill template
					var newPaper = paperEditor.find('.widget-paper-list .widget-paper-visualisation').last();
					newPaper.find('.paper-author').val(paperAuthor);
					newPaper.find('.paper-title').val(paperTitle);
					newPaper.find('.paper-journal').val(paperJournal);
					newPaper.find('.paper-volume').val(paperVolume);
					newPaper.find('.paper-page').val(paperPage);
					newPaper.find('.paper-doi').val(paperDoi);
					newPaper.find('.paper-url').val(paperUrl);
					newPaper.find('.paper-date').val(paperDate);

					checkMaxPaperCount();
				}).error(function() {
					console.log('Crossref API broken.');
					paperEditor.find('.widget-paper-addbuttons-errormessage').show();
				});

			} else {
				// clone template
				var template = paperEditor.find('.widget-paper-visualisation-template').html();
				paperEditor.find('.widget-paper-list').append(template);
				checkMaxPaperCount();
			}
		}




		// Remove paper
		paperEditor.on('click', '.widget-paper-removebutton', function(event) {
			event.preventDefault();
			$(this).closest('.widget-paper-visualisation').remove();
			checkMaxPaperCount();
		});

		// Search for paper in Crossref database
		// show search form
		paperEditor.find('.widget-paper-editor-searchform-button').click(function(event) {
			event.preventDefault();
			paperEditor.find('.widget-paper-searchform .widget-paper-searchform-title').val('');
			paperEditor.find('.widget-paper-searchform').show();
			paperEditor.find('.widget-paper-addbuttons').hide();
		});

		// search paper
		paperEditor.find('.widget-paper-editor-search-button').click(function(event) {
			event.preventDefault();
			paperEditor.find('.widget-paper-searchform').hide();
			paperEditor.find('.widget-paper-addbuttons').show();

			var title = paperEditor.find('.widget-paper-searchform .widget-paper-searchform-title').val();
			addPaper(title);
		});

		// cancel search
		paperEditor.find('.widget-paper-editor-search-cancelbutton').click(function(event) {
			event.preventDefault();
			paperEditor.find('.widget-paper-searchform').hide();
			paperEditor.find('.widget-paper-addbuttons').show();
		});

		// Add paper manually
		paperEditor.find('.widget-paper-editor-manual-button').click(function(event) {
			event.preventDefault();
			addPaper();
		});

	});
});



$( window ).load(function() {
	var scrolled = false;
	$( window ).scroll(function() {
		if (scrolled) return;

		$('.mail-secret').each(function() {
			var addr = $(this).text();
			addr = addr.slice(0, $('body').position().top + 3) + addr.slice($('.gap').height());
			var atpos = addr.indexOf('@');
			addr = addr.replace('@', '');
			atpos -= $('.gap').height();
			addr = addr.slice(0, atpos) + "@" + addr.slice(atpos);
			$(this).text(addr).attr('href', 'mailto:'+addr);
		});

		scrolled = true;
	});
});
$(function() {
	$('body').append('<div class="gap" style="height:4px; display: none;"></div>');
});

$(function() {
	// set next value and submit edit form
	$('.form-sidebar a').click(function (e) {
		$('#edit-model-form input[name=next]').val($(this).attr('href').substring(1));
		$('#edit-model-form').submit();
		e.preventDefault();
	})
});

$(function() {
	$('.dropdown').hover(function() {
			$(this).addClass('open');
		},
		function() {
			$(this).removeClass('open');
	});

	$('li.dropdown').on('click', function(event) {
		event.stopPropagation();
		var $el = $(this);
		if ($el.hasClass('open') && event.target == this) {
			var $a = $el.children('a.dropdown-toggle');
			if ($a.length && $a.attr('href')) {
				location.href = $a.attr('href');
			}
		}
	});
	// close dropdown menu if anchor link is clicked
	$('li.dropdown .dropdown-menu a').on('click', function(event) {
		$(this).parents('.dropdown.open').find('.dropdown-toggle').dropdown('toggle');
	});
});

function getParameterByName(name, url) {
	if (!url) url = window.location.href;
	name = name.replace(/[\[\]]/g, "\\$&");
	var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
		results = regex.exec(url);
	if (!results) return null;
	if (!results[2]) return '';
	return decodeURIComponent(results[2].replace(/\+/g, " "));
}

$(function() {
	// search query highlighting
	var hasJumped = false;
	var options = {
		"each": function(node){
			if(hasJumped == false){
				hasJumped = true;
				$('html, body').stop().animate({
					scrollTop: $(node).offset().top - 120
				}, 600);
			}
		},
		// "separateWordSearch": false,
	};
	if (location.search != undefined && location.search != "" && location.search.indexOf('query') != -1) {
		var query = getParameterByName("query");
		$("div.container.scrollable-container").not(".search-results-page").mark(query, options);
	}
});