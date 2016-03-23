# -*- coding: utf-8 -*-
# # Data for the styleguide context
#

data = {
    'messages': {
        'name': 'Messages',
        'template': 'widgets/messages.html',
        'context': {
            'messages': [
                {
                    'tags': 'info',
                    'text': 'Swag. Low alda.',
                },
                {
                    'tags': 'success',
                    'text': 'Yolo! Läuft.',
                },
                {
                    'tags': 'warning',
                    'text': 'Warnung! Alle Mann Panik!',
                },
                {
                    'tags': 'error',
                    'text': 'Fehler! Schlimmste Gefahr!',
                },
                {
                    'text': 'Random stuff',
                },
            ],
        },
    },


    'header': {
        'name': 'Header',
        'template': 'widgets/header.html',
        'context': {
            'id': '1',
            'links': [
                { 'url': 'http://google.de/1', 'text': 'About' },
                { 'url': 'http://bing.de/2', 'text': 'Getting started' },
                { 'url': 'http://bing.de/3', 'text': 'Impact Models', 'active': True, },
                { 'url': 'http://bing.de/4', 'text': 'Output Data' },
                { 'url': 'http://bing.de/5', 'text': 'Outcomes' },
                { 'url': 'http://bing.de/6', 'text': 'FAQ' },
            ],
        },
    },


    'teaser': {
        'name': 'Teaser',
        'template': 'widgets/teaser.html',
        'context': {
            'title': 'Teaser',
            'text': 'Sed ut perspiciatis unde omnis iste natus error sit\nvoluptatem accusantium doloremque laudantium. ',
            'button': {
                'url': 'http://google.ru',
                'text': 'Facebook',
                'fontawesome': 'facebook',
            },
        },
    },


    'breadcrumb': {
        'name': 'Breadcrumb',
        'template': 'widgets/breadcrumb.html',
        'context': {
            'links': [
                { 'url': 'http://google.de', 'text': 'Kontakt' },
                { 'url': 'http://bing.de', 'text': 'Presse' },
                { 'url': 'http://bing.de', 'text': 'Zwischenseite' },
                { 'url': 'http://google.de', 'text': 'Newsletter', 'active': True },
            ],
        },
    },


    'heading1': {
        'name': 'Heading 1',
        'template': 'widgets/heading1.html',
        'context': {
            'text': 'Besuch des Bürgermeisters',
        },
    },
    'heading2': {
        'name': 'Heading 2',
        'template': 'widgets/heading2.html',
        'context': {
            'text': 'Die Fotografie von Geistern',
        },
    },
    'heading3': {
        'name': 'Heading 3',
        'template': 'widgets/heading3.html',
        'context': {
            'text': 'Die Fotografie von Geistern',
        },
    },



}