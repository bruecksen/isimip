/* Project specific Javascript goes here. */

$(function() {
	// Handler for .ready() called.
});


$(function () {
	$('.leaflet-map').each(function(i) {
		var mapdata = window.mapdata; // Hmm warum ist mapdata nicht sowieso global?

		// Karten auf der Seite durchnummerieren
		var mapid = 'leaflet-map-' + (i+1);
		$(this).attr('id', mapid );

		// Interaktion abschalten bis auf Popups von Map-Markern
		if ($(this).hasClass('leaflet-map-nointeraction')) {
			var options = { zoomControl:false };
		} else {
			var options = {};
		}

		var lat = $(this).data('lat');
		var lon = $(this).data('lon');
		var popup = $(this).data('popup');

		if (lat) {
			// Wenn kein Marker direkt angegeben ist, muss es ein Javascript-Objekt marker mit Markern geben.
			var mapdata = {
				'pins': [ {
					'lat': lat,
					'lon': lon,
					'popup': popup,
				} ],
				'view': {
					'lat': lat,
					'lon': lon,
					'zoom': 11,
				}
			};
		} else if (!mapdata) {
			console.log("mapdata missing");
			return;
		}

		var map = L.map(mapid, options).setView([mapdata.view.lat, mapdata.view.lon], mapdata.view.zoom);

		// var tiles = 'http://c.tiles.wmflabs.org/osm-no-labels/{z}/{x}/{y}.png'; // No labels
		var tiles = 'http://{s}.tile.osm.org/{z}/{x}/{y}.png'; // Regular
		L.tileLayer(tiles, {
				attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
		}).addTo(map);

		if ($(this).hasClass('leaflet-map-nointeraction')) {
			map.dragging.disable();
			map.touchZoom.disable();
			map.doubleClickZoom.disable();
			map.scrollWheelZoom.disable();
			map.boxZoom.disable();
			map.keyboard.disable();
			if (map.tap) map.tap.disable();
		}

		var icon = L.icon({
			iconUrl: '/static/images/map-marker.png',
			shadowUrl: '/static/images/map-marker-shadow.png',
			iconSize: [33, 33],
			iconAnchor: [17, 17],
			popupAnchor: [1, -34],
			shadowSize: [41, 41]
		});


		var markers = [];
		$.each(mapdata.pins, function(i, markerdata) {
			var marker = L.marker([markerdata.lat, markerdata.lon], {icon: icon}).addTo(map).bindPopup(markerdata.popup);
			if ($(this).hasClass('leaflet-map-nointeraction')) {
				marker.on("popupclose", function(e) {
					map.setView([mapdata.view.lat, mapdata.view.lon], mapdata.view.zoom);
				});
			}
			markers.push( marker );
		});
		// Fit map to marker bounds
		var markergroup = new L.featureGroup(markers);
		map.fitBounds(markergroup.getBounds(), { 'maxZoom': 15 });




		function addClosebutton(map, href) {
			// Close Button
			// http://gis.stackexchange.com/questions/127286/home-button-leaflet-map
			L.Control.closebutton = L.Control.extend({
				options: {
					position: 'topright',
					title: 'Schließen',
					text: '<i class="fa fa-times"></i>',
					href: href,
				},

				onAdd: function (map) {
					var container = L.DomUtil.create('div', 'closebutton leaflet-bar'),
						options = this.options;


					this._closeButton = L.DomUtil.create('a', 'closebutton', container);
					this._closeButton.innerHTML = options.text;
					this._closeButton.href = options.href;
					this._closeButton.title = options.title;

					return container;
				},

				onRemove: function (map) {
				},

			});
			// add the new closebutton to the map
			var closebutton = new L.Control.closebutton();
			closebutton.addTo(map);
		}
		if ($(this).data('closebuttonhref')) {
			addClosebutton(map, $(this).data('closebuttonhref'));
		}


	});

}); // leaflet


$(window).on('station-booking-form-loaded', function () {
	if ( !$('#station-booking-form').length ) {
		return;
	}

	// Dieses Feld soll gesendet, aber nicht angezeigt werden. Es enthält die auswählbaren Termine.
	$('#div_id_appointment').hide();


	// Zeit-Auswahl
	$('select#id_time').change(function() {
		var value = $(this).val();
		$('select#id_appointment').val( value );
	});


	// Datum-Auswahl
	$('select#id_date').change(function() {
		// Get rid of old times
		$('select#id_time option').remove();
		// Offer new times
		$.each(appointments, function(i, appointment) {
			var time = appointment.time;
			var day = time.getFullYear() + '-' + ("0" + time.getMonth()).slice(-2) + '-' + ("0" + time.getDate()).slice(-2);
			if ($('select#id_date').val() == day) {
				var value = appointment.value;
				var timeGerman = time.getHours() + ':' + ("0" + time.getMinutes()).slice(-2);
				$('select#id_time').append('<option value="'+ value +'">'+ timeGerman +'</option>');
			}
		});
		$('select#id_time').change().prop('selectedIndex', -1);
	});


	// Generiere ein Array mit den Zeiten, die ausgewählt werden können
	var appointments = [];

	$('select#id_appointment option').each(function() {
		var time = $(this).text();
		time = new Date( time );
		var value = $(this).attr('value');
		if (time && value) {
			appointments.push({ 'time': time, 'timestring': time.toString(), 'value': value });

			var day = time.getFullYear() + '-' + ("0" + time.getMonth()).slice(-2) + '-' + ("0" + time.getDate()).slice(-2);
			var dayGerman = time.getDate() + '.&#8239;' + time.getMonth() + '.&#8239;' + time.getFullYear();

			if (!$('select#id_date option[value="'+ day +'"]').length > 0) {
				// Den Tag gibt es noch nicht zur Auswahl
				$('select#id_date').append('<option value="'+ day +'">'+ dayGerman +'</option>');
			}
		}
	});

	// Initialize SELECT fields
	$('select#id_date').change().prop('selectedIndex', -1);
	$('select#id_time option').remove();
}); // station-booking-form



$(function() {
	$('.widget-flickr').each(function() {
		var flickrwidget = $(this);

		var limit = encodeURIComponent( flickrwidget.data('limit') );
		var userid = encodeURIComponent( flickrwidget.data('userid') );
		var apikey = encodeURIComponent( flickrwidget.data('apikey') );
		var url = "https://api.flickr.com/services/rest/?method=flickr.people.getPublicPhotos&api_key="+ apikey +"&user_id="+ userid +"&per_page="+ limit +"&format=json&jsoncallback=?";
		$.getJSON( url, function( data ) {
			if (data.stat != 'ok') {
				flickrwidget.html('<h3>Bilder konnten nicht geladen werden.</h3>');
				console.log('Flickr-Daten', url, data);
				return;
			}
			$.each(data.photos.photo, function( i, photo ) {
				var photoURL = 'http://farm' + photo.farm + '.static.flickr.com/' + photo.server + '/' + photo.id + '_' + photo.secret + '_c.jpg';
				flickrwidget.append('<a href="http://flickr.com/photo.gne?id=' + photo.id + '" target="_blank"><img src="' + photoURL + '" class="image"></a>');
			});
		});
	});
});



$(function() {
	$('.widget-carousel').each(function() {
		var carousel = $(this);
		// Image missing or only one image in carousel?
		if (carousel.find('.widget-carousel-images-image').length < 2) { return; }

		// Hide all images that are behind current image
		carousel.find('.widget-carousel-images-image:not(:first)').hide();

		// Loop show
		setInterval(function() {
			// Loop images
			var currentimage = carousel.find('.widget-carousel-images-image:visible');
			var nextimage = currentimage.next();
			if (!nextimage.length) {
				nextimage = carousel.find('.widget-carousel-images-image').first();
			}

			currentimage.delay(500).fadeOut(300);
			nextimage.fadeIn(300);
		}, 6000);
	});
});


