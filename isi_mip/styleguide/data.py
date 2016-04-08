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


    'head_super': {
        'name': 'Super in Head',
        'template': 'widgets/head-super.html',
        'context': {
            'title': 'Teaser',
            'text': 'Sed ut perspiciatis unde omnis iste natus error sit\nvoluptatem accusantium doloremque laudantium. ',
            'button': {
                'href': 'http://google.ru',
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
    'heading3a': {
        'name': 'Heading 3',
        'template': 'widgets/heading3.html',
        'context': {
            'text': 'Getting started',
        },
    },
    'heading3b': {
        'name': 'Heading 3',
        'template': 'widgets/heading3.html',
        'context': {
            'text': 'Impact Models',
        },
    },
    'heading3c': {
        'name': 'Heading 3',
        'template': 'widgets/heading3.html',
        'context': {
            'text': 'Output Data',
        },
    },
    'heading3d': {
        'name': 'Heading 3',
        'template': 'widgets/heading3.html',
        'context': {
            'text': 'Outcomes',
        },
    },



    'columns_1_1': {
        'name': 'Columns 1:1',
        'template': 'widgets/columns-1-1.html',
        'context': {
            'left_column': '<h2 style="background-color: #eee;">Left Column</h2>',
            'right_column': '<h2 style="background-color: #eee;">Right Column</h2>',
        },
    },
    'columns_2_1': {
        'name': 'Columns 2:1',
        'template': 'widgets/columns-2-1.html',
        'context': {
            'left_column': '<h2 style="background-color: #eee;">Left Column</h2>',
            'right_column': '<h2 style="background-color: #eee;">Right Column</h2>',
        },
    },
    'columns_1_2': {
        'name': 'Columns 1:2',
        'template': 'widgets/columns-1-2.html',
        'context': {
            'left_column': '<h2 style="background-color: #eee;">Left Column</h2>',
            'right_column': '<h2 style="background-color: #eee;">Right Column</h2>',
        },
    },
    'columns_1_1_1': {
        'name': 'Columns 1:1:1',
        'template': 'widgets/columns-1-1-1.html',
        'context': {
            'left_column': '<h2 style="background-color: #eee;">Left Column</h2>',
            'center_column': '<h2 style="background-color: #eee;">Center Column</h2>',
            'right_column': '<h2 style="background-color: #eee;">Right Column</h2>',
        },
    },
    'columns_1_1_1_1': {
        'name': 'Columns 1:1:1:1',
        'template': 'widgets/columns-1-1-1-1.html',
        'context': {
            'first_column': '<h2 style="background-color: #eee;">First Column</h2>',
            'second_column': '<h2 style="background-color: #eee;">Second Column</h2>',
            'third_column': '<h2 style="background-color: #eee;">Third Column</h2>',
            'fourth_column': '<h2 style="background-color: #eee;">Fourth Column</h2>',
        },
    },




    'image': {
        'name': 'Image',
        'template': 'widgets/image.html',
        'context': {
            'url': '/static/styleguide/test-images/header1-3by1.jpg',
            'name': 'Meere und Ozeane',
        },
    },

    'image_link': {
        'name': 'Image with Link',
        'template': 'widgets/image.html',
        'context': {
            'url': '/static/styleguide/test-images/header2-3by1.jpg',
            'name': 'Meere und Ozeane',
            'href': 'http://xxx',
        },
    },


    'arrow_right_link': {
        'name': 'Arrow Right Link',
        'template': 'widgets/arrow-right-link.html',
        'context': {
            'href': 'http://bing.de/',
        },
    },




    'richtext': {
        'name': 'Richtext',
        'template': 'widgets/richtext-content.html',
        'context': {
            'content': '<div class="rich-text"><p><img class="richtext-image right" src="/static/styleguide/test-images/header3.jpg" alt="Schönes Bild">Jemand musste Josef K. verleumdet haben, denn ohne dass er etwas Böses getan hätte, wurde er <a href="#">eines Morgens</a> verhaftet. »Wie ein Hund!« sagte er, es war, als sollte die Scham ihn überleben. Als Gregor Samsa eines Morgens aus unruhigen Träumen erwachte, fand er sich in seinem Bett zu einem ungeheueren Ungeziefer verwandelt. Und es war ihnen wie eine Bestätigung ihrer neuen Träume und guten Absichten, als am Ziele ihrer Fahrt die Tochter als erste sich erhob und ihren jungen Körper dehnte. »Es ist ein eigentümlicher Apparat«, sagte der Offizier zu dem Forschungsreisenden und überblickte mit einem gewissermaßen bewundernden Blick den ihm doch wohlbekannten Apparat. Sie hätten noch ins Boot springen können, aber der Reisende hob ein schweres, geknotetes Tau vom Boden, drohte ihnen damit und hielt sie dadurch von dem Sprunge ab.</p><div style="padding-bottom: 56.25%;" class="responsive-object"><iframe src="https://www.youtube.com/embed/SywPPK8ixiw?feature=oembed" allowfullscreen="" width="480" frameborder="0" height="270"></iframe></div><h3>Yolo!</h3><p>Jemand musste Josef K. verleumdet haben, denn ohne dass er etwas Böses getan hätte, wurde er eines Morgens verhaftet. »Wie ein Hund!« sagte er, es war, als sollte die Scham ihn überleben. Als Gregor Samsa eines Morgens aus unruhigen Träumen erwachte, fand er sich in seinem Bett zu einem ungeheueren Ungeziefer verwandelt. Und es war ihnen wie eine Bestätigung ihrer neuen Träume und guten Absichten, als am Ziele ihrer Fahrt die Tochter als erste sich erhob und ihren jungen Körper dehnte. »Es ist ein eigentümlicher Apparat«, sagte der Offizier zu dem Forschungsreisenden und überblickte mit einem gewissermaßen bewundernden Blick den ihm doch wohlbekannten Apparat. Sie hätten noch ins Boot springen können, aber der Reisende hob ein schweres, geknotetes Tau vom Boden, drohte ihnen damit und hielt sie dadurch von dem Sprunge ab.</p></div>',
        },
    },

    'embed': {
        'name': 'Embed',
        'template': 'widgets/embed.html',
        'context': {
            'embed': '<div style="padding-bottom: 56.25%;" class="responsive-object"><iframe src="https://www.youtube.com/embed/BrPYsOhRj4I?feature=oembed" allowfullscreen="" width="480" frameborder="0" height="270"></iframe></div>',
        },
    },


    'page_teaser_text': {
        'name': 'Page Teaser Text (use only in other page-teaser templates)',
        'template': 'widgets/page-teaser-text.html',
        'context': {
            'href': 'http://bing.de/',
            'title': 'Getting started',
            'description': 'Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum',
            'arrow_right_link': True,
        },
    },


    'page_teaser': {
        'name': 'Page Teaser',
        'template': 'widgets/page-teaser.html',
        'context': {
            'href': 'http://bing.de/',
            'image': {
                'url': '/static/styleguide/test-images/dog.jpg',
            },
            'title': 'Output Data',
            'description': 'Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum',
            'arrow_right_link': True,
        },
    },

    'page_teaser_noimage': {
        'name': 'Page Teaser no Image',
        'template': 'widgets/page-teaser.html',
        'context': {
            'href': 'http://bing.de/',
            'title': 'Input Data',
            'description': 'Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusm iste doloremque. Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusm iste doloremque. Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusm iste doloremque. Sed ut perspiciatis unde omnis iste natus error sit.',
            'arrow_right_link': True,
        },
    },


    'page_teaser_notitle': {
        'name': 'Page Teaser',
        'template': 'widgets/page-teaser.html',
        'context': {
            'href': 'http://bing.de/',
            'image': {
                'url': '/static/styleguide/test-images/dog.jpg',
            },
            'description': 'Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum',
            'arrow_right_link': True,
        },
    },


    'page_teaser_wide': {
        'name': 'Page Teaser Wide',
        'template': 'widgets/page-teaser-wide.html',
        'context': {
            'href': 'http://bing.de/',
            'image': {
                'url': '/static/styleguide/test-images/silhouette.jpg',
            },
            'title': 'Impact Models',
            'date': '8/12/2016',
            'description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui.',
            'arrow_right_link': True,
        },
    },


    'page_teaser_wide_wideimage': {
        'name': 'Page Teaser Wide with wide image',
        'template': 'widgets/page-teaser-wide.html',
        'context': {
            'href': 'http://bing.de/',
            'wideimage': True,
            'image': {
                'url': '/static/styleguide/test-images/header3-3by1.jpg',
            },
            'title': 'Impact Models',
            'datebeforetitle': True,
            'date': '8/12/2016',
            'divider': True,
            'description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui.',
            'arrow_right_link': False,
            'text_right_link': True,
            'text_right_link_text': 'Learn more',
        },
    },


    'page_teaser_paper': {
        'name': 'Page Teaser Paper',
        'template': 'widgets/page-teaser.html',
        'context': {
            'image': {
                'url': '/static/styleguide/test-images/header4.jpg',
            },
            'author': 'Prof. Dr. Motte et al',
           'title': 'Impact Models in an industrialized semipermeable meta world',
            'journal': 'Biotech Publishing 7/2016, 2834ff',
            'description': 'Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum',
            'source': {
                'description': 'http://www.ncbi.nlm.nih.gov/pmc/articles/PMC3178846/',
                'href': 'http://www.ncbi.nlm.nih.gov/pmc/articles/PMC3178846/',
            },
            'arrow_right_link': True,
        },
    },



    'page_teaser_flat': {
        'name': 'Page Teaser Flat',
        'template': 'widgets/page-teaser-flat.html',
        'context': {
            'date': '8/12/2016',
            'title': 'Impact Models in an industrialized semipermeable meta world',
            'description': 'Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum',
        },
    },



    'download_link': {
        'name': 'Download Link',
        'template': 'widgets/download-link.html',
        'context': {
            'button': {
                'href': 'https://www.mozilla.org/de/firefox/new/',
                'text': 'Download',
            },
            'description': 'Download PDF Mission / Implementation',
            'fontawesome': 'file-pdf-o',
        },
    },




    'indicator': {
        'name': 'Indicator',
        'template': 'widgets/indicator.html',
        'context': {
            'number': '17&#8239;000',
            'title': 'Indicator swag',
            'text': 'Sed ut perspiciatis unde omnis iste natus error sit voluptatem  doloremque laudantium.',
        },
    },

    'readmorelink': {
        'name': 'Read more link',
        'template': 'widgets/read-more-link.html',
        'context': {
            'tinyarrow': True,
            'text': 'weiterlesen',
            'url': 'http://x',
        },
    },
    'readmorelink_right': {
        'name': 'Read more link – right align',
        'template': 'widgets/read-more-link.html',
        'context': {
            'text': 'weiterlesen',
            'url': 'http://x',
            'align': 'right',
            'tinyarrow': True,
        },
    },
    'readmorelink_rightarrow': {
        'name': 'Read more link – with arrow',
        'template': 'widgets/read-more-link.html',
        'context': {
            'arrow': True,
            'text': 'weiterlesen',
            'url': 'http://x',
            'align': 'right',
        },
    },
    'readmorelink_download': {
        'name': 'Read more link – Download',
        'template': 'widgets/read-more-link.html',
        'context': {
            'large': True,
            'text': '<i class="fa fa-download"></i> Download',
            'url': 'http://x',
            'align': 'right',
        },
    },

    'horizontal_ruler': {
        'name': 'Horizontal Ruler',
        'template': 'widgets/horizontal-ruler.html',
        'context': {
        },
    },
    'horizontal_ruler_light': {
        'name': 'Horizontal Ruler Light',
        'template': 'widgets/horizontal-ruler.html',
        'context': {
            'light': True,
        },
    },

    'link_list': {
        'name': 'Link List',
        'template': 'widgets/link-list.html',
        'context': {
            'links': [
                { 'fontawesome': 'clock-o', 'prepend': '16.3.2016', 'text': 'Die neue Veröffentlichung', 'href': 'http://google.de', },
                { 'fontawesome': 'file-pdf-o', 'text': 'Die neue Veröffentlichung', 'href': 'http://google.de', },
                { 'prepend': '16.3.2016', 'text': 'Die neue Veröffentlichung', 'href': 'http://google.de', },
                { 'text': 'Die neue Veröffentlichung', 'href': 'http://google.de', },
            ],
        },
    },



    'table': {
        'name': 'Table',
        'template': 'widgets/table.html',
        'context': {
            'head': {
                'cols': [
                    { 'text': 'Data Set', },
                    { 'text': 'Data Type', },
                    { 'text': 'Data set', },
                ],
            },
            'body': {
                'rows': [
                    {
                        'cols': [
                            { 'text': 'princeton watch wfdei', },
                            { 'text': 'Socio Economic', },
                            { 'text': 'Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam. Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam.', },
                        ],
                    },
                    {
                        'cols': [
                            { 'text': 'princeton <a href="http://google.de">watch</a> wfdei', },
                            { 'text': 'Economic Socio', },
                            { 'text': 'Sed ut <a href="http://google.de">perspiciatis unde omnis iste natus error sit</a> voluptatem<br>accusantium doloremque laudantium, totam. Sed ut perspiciatis unde omnis iste natus error sit voluptatem.', },
                        ],
                    },
                    {
                        'cols': [
                            { 'text': 'princeton watch wfdei', },
                            { 'text': 'Climate', },
                            { 'text': '<p>Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam.</p><p>Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam.</p>', },
                        ],
                    },
                ],
            },
        },
    },



    'table_limit': {
        'name': 'Table with row limit',
        'template': 'widgets/table.html',
        'context': {
            'head': {
                'cols': [
                    { 'text': 'Data Set', },
                    { 'text': 'Data Type', },
                    { 'text': 'Data set', },
                ],
            },
            # read all button at end of table
            'showalllink': {
                'buttontext': 'See all <i class="fa fa-chevron-down"></i>',
            },
            'body': {
                'rows': [
                    {
                        'cols': [
                            { 'text': 'princeton watch wfdei', },
                            { 'text': 'Socio Economic', },
                            { 'text': 'Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam. Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam.', },
                        ],
                    },
                    {
                        'cols': [
                            { 'text': 'princeton watch wfdei', },
                            { 'text': 'Economic Socio', },
                            { 'text': 'Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam. Sed ut perspiciatis unde omnis iste natus error sit voluptatem.', },
                        ],
                    },
                    {
                        'invisible': True,
                        'cols': [
                            { 'text': 'princeton watch wfdei', },
                            { 'text': 'Climate', },
                            { 'text': 'Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam. Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam.', },
                        ],
                    },
                    {
                        'invisible': True,
                        'cols': [
                            { 'text': 'princeton watch wfdei', },
                            { 'text': 'Alimate 2', },
                            { 'text': 'Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam. Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam.', },
                        ],
                    },
                    {
                        'invisible': True,
                        'cols': [
                            { 'text': 'princeton watch wfdei', },
                            { 'text': 'Glimac 3', },
                            { 'text': 'Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam. Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam.', },
                        ],
                    },
                ],
            },
        },
    },






    'table_pagination': {
        'name': 'Table with pagination',
        'template': 'widgets/table.html',
        'context': {
            'head': {
                'cols': [
                    { 'text': 'Data Set', },
                    { 'text': 'Data Type', },
                    { 'text': 'Data set', },
                ],
            },
            'pagination': {
                'rowsperpage': 3,
                'numberofpages': 3, # number of pages with current filters
                'pagenumbers': [
                    { 'number': 1, 'invisible': False, },
                    { 'number': 2, 'invisible': False, },
                    { 'number': 3, 'invisible': False, },
                ], 
                'activepage': 2, # set to something between 1 and numberofpages
            },
            'body': {
                'rows': [
                    {
                        'invisible': True,
                        'cols': [
                            { 'text': 'princeton watch wfdei', },
                            { 'text': 'Socio Economic', },
                            { 'text': 'Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam. Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam.', },
                        ],
                    },
                    {
                        'invisible': True,
                        'cols': [
                            { 'text': 'princeton watch wfdei', },
                            { 'text': 'Economic Socio', },
                            { 'text': 'Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam. Sed ut perspiciatis unde omnis iste natus error sit voluptatem.', },
                        ],
                    },
                    {
                        'invisible': True,
                        'cols': [
                            { 'text': 'princeton watch wfdei', },
                            { 'text': 'Climate F', },
                            { 'text': 'Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam. Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam.', },
                        ],
                    },
                    {
                        'cols': [
                            { 'text': 'princeton watch wfdei', },
                            { 'text': 'Alimate 2 E', },
                            { 'text': 'Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam. Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam.', },
                        ],
                    },
                    {
                        'cols': [
                            { 'text': 'princeton watch wfdei', },
                            { 'text': 'Glimac 3 Z', },
                            { 'text': 'Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam. Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam.', },
                        ],
                    },
                    {
                        'cols': [
                            { 'text': 'princeton watch wfdei', },
                            { 'text': 'Alimate 2 W', },
                            { 'text': 'Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam. Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam.', },
                        ],
                    },
                    {
                        'invisible': True,
                        'cols': [
                            { 'text': 'princeton watch wfdei', },
                            { 'text': 'Glimac 3 Q', },
                            { 'text': 'Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam. Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam.', },
                        ],
                    },
                ],
            },
        },
    },





    'table_selector': {
        'name': 'Filter for Table',
        'template': 'widgets/table-selector.html',
        'context': {
            'tableid': 'selectortable',
            'selectors': [
                {
                    'colnumber': '2', # column number in table starting with 1
                    'all_value': 'All regions',
                    'options': [
                        { 'value': 'Berlin' },
                        { 'value': 'Brandenburg' },
                        { 'value': 'Hamburg' },
                        { 'value': 'Bremen' },
                        { 'value': 'Milano' },
                        { 'value': 'Venezia' },
                        { 'value': 'Düsseldorf' },
                    ],
                },
                {
                    'colnumber': '3',
                    'all_value': 'All countries',
                    'activeoption': 'Deutschland',
                    'options': [
                        { 'value': 'Deutschland' },
                        { 'value': 'France' },
                        { 'value': 'Italia' },
                    ],
                },
            ],
            'searchfield': {
                'value': '',
            },
        },
    },



    'table_pagination_filter': {
        'name': 'Table with pagination and filter',
        'template': 'widgets/table.html',
        'context': {
            'id': 'selectortable',
            'head': {
                'cols': [
                    { 'text': 'Town', },
                    { 'text': 'Region', },
                    { 'text': 'Country', },
                    { 'text': 'Continent', },
                    { 'text': 'Wind direction', },
                ],
            },
            'filter': '{ "3": "Deutschland" }', # pre defined filter
            'pagination': {
                'rowsperpage': 3,
                'numberofpages': 3, # number of pages with current filters
                'pagenumbers': [
                    { 'number': 1, 'invisible': False, },
                    { 'number': 2, 'invisible': False, },
                    { 'number': 3, 'invisible': False, },
                    { 'number': 4, 'invisible': True, },
                    { 'number': 5, 'invisible': True, },
                ], 
                'activepage': 1, # set to something between 1 and numberofpages
            },
            'norowvisible': False, # true when no row is visible
            'body': {
                'rows': [
                    {
                        'invisible': False,
                        'cols': [
                            { 'text': 'Berlin', },
                            { 'text': 'Berlin', },
                            { 'text': 'Deutschland', },
                            { 'text': 'Europe', },
                            { 'text': 'North', },
                        ],
                    },
                    {
                        'invisible': False,
                        'cols': [
                            { 'text': 'München', },
                            { 'text': 'Bayern', },
                            { 'text': 'Deutschland', },
                            { 'text': 'Europe', },
                            { 'text': 'North West', },
                        ],
                    },
                    {
                        'invisible': False,
                        'cols': [
                            { 'text': 'Hamburg', },
                            { 'text': 'Hamburg', },
                            { 'text': 'Deutschland', },
                            { 'text': 'Europe', },
                            { 'text': 'West', },
                        ],
                    },
                    {
                        'invisible': True,
                        'cols': [
                            { 'text': 'Belzig', },
                            { 'text': 'Brandenburg', },
                            { 'text': 'Deutschland', },
                            { 'text': 'Europe', },
                            { 'text': 'West', },
                        ],
                    },
                    {
                        'invisible': True,
                        'cols': [
                            { 'text': 'Wollin', },
                            { 'text': 'Brandenburg', },
                            { 'text': 'Deutschland', },
                            { 'text': 'Europe', },
                            { 'text': 'East', },
                        ],
                    },
                    {
                        'invisible': True,
                        'cols': [
                            { 'text': 'Frankfurt Oder', },
                            { 'text': 'Brandenburg', },
                            { 'text': 'Deutschland', },
                            { 'text': 'Europe', },
                            { 'text': 'East', },
                        ],
                    },
                    {
                        'invisible': True,
                        'cols': [
                            { 'text': 'Bremen', },
                            { 'text': 'Bremen', },
                            { 'text': 'Deutschland', },
                            { 'text': 'Europe', },
                            { 'text': 'East', },
                        ],
                    },
                    {
                        'invisible': True,
                        'cols': [
                            { 'text': 'Bremerhaven', },
                            { 'text': 'Bremen', },
                            { 'text': 'Deutschland', },
                            { 'text': 'Europe', },
                            { 'text': 'East', },
                        ],
                    },
                    {
                        'invisible': True,
                        'cols': [
                            { 'text': 'Paris', },
                            { 'text': 'Paris', },
                            { 'text': 'France', },
                            { 'text': 'Europe', },
                            { 'text': 'South West', },
                        ],
                    },
                    {
                        'invisible': True,
                        'cols': [
                            { 'text': 'Milano', },
                            { 'text': 'Milano', },
                            { 'text': 'Italia', },
                            { 'text': 'Europe', },
                            { 'text': 'South', },
                        ],
                    },
                    {
                        'invisible': True,
                        'cols': [
                            { 'text': 'Venezia', },
                            { 'text': 'Milano', },
                            { 'text': 'Italia', },
                            { 'text': 'Europe', },
                            { 'text': 'East', },
                        ],
                    },
                    {
                        'invisible': True,
                        'cols': [
                            { 'text': 'Düsseldorf', },
                            { 'text': 'Nordrhein-Westfalen', },
                            { 'text': 'Deutschland', },
                            { 'text': 'Europe', },
                            { 'text': 'North West', },
                        ],
                    },
                ],
            },
        },
    },




    'expandable': {
        'name': 'Expandable',
        'template': 'widgets/expandable.html',
        'context': {
            'headline': 'FAQ for researchers',
            'border': True,
            'list': [
                { 'term': 'Sed ut perspiciatis?', 'definition': 'Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque. Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque. Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque', },
                { 'term': 'Sed ut perspiciatis unde omnis iste natus error sit?', 'definition': 'Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque. Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque. Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque', 'opened': True, },
                { 'term': 'Sed ut perspiciatis unde omnis iste?', 'definition': 'Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque. Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque. Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque', 'opened': True, 'notoggle': True, },
            ],
        },
    },


    'footer': {
        'name': 'Footer',
        'template': 'widgets/footer.html',
        'context': {
            'links': [
                { 'url': 'http://google.de', 'text': 'Kontakt' },
                { 'url': 'http://bing.de', 'text': 'Presse', 'active': True },
                { 'url': 'http://google.de', 'text': 'Newsletter' },
            ],
        },
    },

}