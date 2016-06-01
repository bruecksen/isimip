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
            'noborder': True,
            'links': [
                {'url': 'http://google.de/1', 'text': 'About'},
                {'url': 'http://bing.de/2', 'text': 'Getting started'},
                {'url': 'http://bing.de/3', 'text': 'Impact Models', 'active': True,},
                {'url': 'http://bing.de/4', 'text': 'Output Data'},
                {'url': 'http://bing.de/5', 'text': 'Outcomes'},
                {'url': 'http://bing.de/6', 'text': 'FAQ'},
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
                {'href': 'http://google.de', 'text': 'Kontakt'},
                {'href': 'http://bing.de', 'text': 'Presse'},
                {'href': 'http://bing.de', 'text': 'Zwischenseite'},
                {'text': 'Newsletter' },
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
    'heading2_link': {
        'name': 'Heading 2 with link',
        'template': 'widgets/heading2.html',
        'context': {
            'text': 'Die Fotografie von Geistern',
            'href': 'http://linkausheading',
        },
    },
    'heading2_smtwolines': {
        'name': 'Heading 2 with two lines in SM',
        'template': 'widgets/heading2.html',
        'context': {
            'widget_heading_sm_two_lines': True,
            'text': 'Fotografie',
        },
    },
    'heading3': {
        'name': 'Heading 3',
        'template': 'widgets/heading3.html',
        'context': {
            'text': 'Die Fotografie von Geistern',
        },
    },
    'heading3_link': {
        'name': 'Heading 3 with link',
        'template': 'widgets/heading3.html',
        'context': {
            'text': 'Die Fotografie von Geistern',
            'href': 'http://linkausheading',
        },
    },
    'heading3_slug': {
        'name': 'Heading 3 with Slug',
        'template': 'widgets/heading3.html',
        'context': {
            'text': 'Die Fotografie von Geistern',
            'slug': 'Heading No Three',
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
            'description': 'Magicgrow Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum',
            'arrow_right_link': True,
            'magicgrow': True,
        },
    },

    'page_teaser_noimage': {
        'name': 'Page Teaser no Image',
        'template': 'widgets/page-teaser.html',
        'context': {
            'href': 'http://bing.de/',
            'title': 'Input Data',
            'description': 'Magicgrow Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusm iste doloremque. Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusm iste doloremque. Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusm iste doloremque. Sed ut perspiciatis unde omnis iste natus error sit.',
            'arrow_right_link': True,
            'magicgrow': True,
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


    'page_teaser_notitle_noimage': {
        'name': 'Page Teaser',
        'template': 'widgets/page-teaser.html',
        'context': {
            'href': 'http://bing.de/',
            'description': 'Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum',
            'arrow_right_link': True,
            'border': True,
        },
    },



    'page_teaser_notitle_noimage_externallink': {
        'name': 'Page Teaser',
        'template': 'widgets/page-teaser.html',
        'context': {
            'href': 'http://bing.de/',
            'description': 'Magicgrow Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum',
            'external_link': True,
            'external_link_text': 'Link to paper',
            'border': True,
            'magicgrow': True,
        },
    },


    'page_teaser_notitle_extratext': {
        'name': 'Page Teaser',
        'template': 'widgets/page-teaser.html',
        'context': {
            'image': {
                'url': '/static/styleguide/test-images/dog.jpg',
            },
            'title': 'Agriculture Sector',
            'description': '<p><strong>Magicgrow Musterfrau</strong><br><a href="https://sinnwerkstatt.com/team/">sinnwerkstatt.com/team/</a><br><a href="mailto:yolo@example.com">yolo@example.com</a></p><hr><p><strong>Martha Musterfrau</strong><br><a href="https://sinnwerkstatt.com/team/">sinnwerkstatt.com/team/alle/mitarbeiter/und/innen</a><br><a href="mailto:yolo-extra-lange-adresse@example.com">yoloextralangeadresse@example.com</a></p>',
            'arrow_right_link': True,
            'magicgrow': True,
        },
    },

    'page_teaser_notitle_noimage_norightlink': {
        'name': 'Page Teaser',
        'template': 'widgets/page-teaser.html',
        'context': {
            'href': 'http://bing.de/',
            'description': 'Magicgrow Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum',
            'magicgrow': True,
        },
    },


    'page_teaser_notitle_noimage_textrightlink': {
        'name': 'Page Teaser',
        'template': 'widgets/page-teaser.html',
        'context': {
            'border': True,
            'href': 'http://bing.de/',
            'description': 'Magicgrow Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum Lorem ipsum mit Rand',
            'text_right_link': True,
            'text_right_link_text': 'Learn more',
            'magicgrow': True,
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
            'text_right_link': True,
            'text_right_link_text': 'Learn more',
        },
    },

    'page_teaser_wide_smallimage': {
        'name': 'Page Teaser Wide with small image',
        'template': 'widgets/page-teaser-wide.html',
        'context': {
            'href': 'http://bing.de/',
            'smallimage': True,
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
            'href': 'http://sinnwerkstatt.com/',
        },
    },
    'page_teaser_flat_nodescription': {
        'name': 'Page Teaser Flat no Description',
        'template': 'widgets/page-teaser-flat.html',
        'context': {
            'date': '8/12/2016',
            'title': 'Impact Models in an industrialized semipermeable meta world',
            'href': 'http://sinnwerkstatt.com/',
        },
    },


    'button': {
        'name': 'Button',
        'template': 'widgets/button.html',
        'context': {
            'href': 'https://www.mozilla.org/de/firefox/new/',
            'text': 'Download',
        },
    },
    'button_primary': {
        'name': 'Button Primary',
        'template': 'widgets/button.html',
        'context': {
            'href': 'https://www.mozilla.org/de/firefox/new/',
            'text': 'Download',
            'primary': True,
        },
    },
    'button_secondary': {
        'name': 'Button Secondary',
        'template': 'widgets/button.html',
        'context': {
            'href': 'https://www.mozilla.org/de/firefox/new/',
            'text': 'Download',
            'secondary': True,
        },
    },


    'download_link': {
        'name': 'Download Link',
        'template': 'widgets/download-link.html',
        'context': {
            'button': {
                'href': 'https://www.mozilla.org/de/firefox/new/',
            },
            'description': 'Download PDF Mission / Implementation',
            'fontawesome': 'file-pdf-o',
        },
    },
    'download_link_longtext': {
        'name': 'Download Link',
        'template': 'widgets/download-link.html',
        'context': {
            'button': {
                'href': 'https://www.mozilla.org/de/firefox/new/',
            },
            'description': 'Download PDF Mission / Implementation the documentation of the life, universum and everything else in between just for the lulz and fun.',
            'fontawesome': 'file-pdf-o',
        },
    },
    'download_link_monstertext': {
        'name': 'Download Link',
        'template': 'widgets/download-link.html',
        'context': {
            'button': {
                'href': 'https://www.mozilla.org/de/firefox/new/',
            },
            'description': 'Download PDF Mission / Implementation the documentation of the life, universum and everything else in between just for the lulz and fun. Download PDF Mission / Implementation the documentation of the life, universum and everything else in between just for the lulz and fun. Download PDF Mission / Implementation the documentation of the life, universum and everything else in between just for the lulz and fun.',
            'fontawesome': 'file-pdf-o',
        },
    },
    'download_link_noicon': {
        'name': 'Download Link',
        'template': 'widgets/download-link.html',
        'context': {
            'button': {
                'href': 'https://www.mozilla.org/de/firefox/new/',
            },
            'description': 'Download PDF Mission / Implementation the documentation of the life, universum and everything else in between just for the lulz and fun.',
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
                {'fontawesome': 'clock-o', 'prepend': '16.3.2016', 'text': 'Die neue Veröffentlichung',
                 'href': 'http://google.de',},
                {'fontawesome': 'file-pdf-o', 'text': 'Die neue Veröffentlichung', 'href': 'http://google.de',},
                {'prepend': '16.3.2016', 'text': 'Die neue Veröffentlichung', 'href': 'http://google.de',},
                {'text': 'Die neue Veröffentlichung', 'href': 'http://google.de',},
            ],
        },
    },

    'pagination_standalone': {
        'name': 'Pagination Standalone',
        'template': 'widgets/pagination-standalone.html',
        'context': {
            'prevbutton_href': 'http://sinnwerkstatt.com',
            'nextbutton_href': 'http://sinnwerkstatt.com',
        },
    },

    'pagination': {
        'name': 'Pagination',
        'template': 'widgets/pagination.html',
        'context': {
            'pagination': {
                'numberofpages': 3,  # number of pages with current filters
                'pagenumbers': [
                    {'number': 1, 'invisible': False,},
                    {'number': 2, 'invisible': False,},
                    {'number': 3, 'invisible': False,},
                    {'number': 4, 'invisible': True,},
                ],
                'activepage': 2,  # set to something between 1 and numberofpages
            },
        },
    },

    'table': {
        'name': 'Table',
        'template': 'widgets/table.html',
        'context': {
            'head': {
                'cols': [
                    {'text': 'Data Set',},
                    {'text': 'Data Type',},
                    {'text': 'Data set',},
                ],
            },
            'body': {
                'rows': [
                    {
                        'cols': [
                            {'texts': ['princeton watch wfdei',], },
                            {'texts': ['Socio Economic',],},
                            {'texts': ['Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam. Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam.',],},
                        ],
                    },
                    {
                        'cols': [
                            {'texts': ['princeton <a href="http://google.de">watch</a> wfdei',],},
                            {'texts': ['Economic Socio',],},
                            {'texts': ['Sed ut <a href="http://google.de">perspiciatis unde omnis iste natus error sit</a> voluptatem<br>accusantium doloremque laudantium, totam. Sed ut perspiciatis unde omnis iste natus error sit voluptatem.',],},
                        ],
                    },
                    {
                        'cols': [
                            {'texts': ['princeton watch wfdei',],},
                            {'texts': ['Climate',],},
                            {'texts': ['<p>Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam.</p>', '<p>Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam.</p>',],},
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
                    {'text': 'Data Set',},
                    {'text': 'Data Type',},
                    {'text': 'Data set',},
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
                            {'texts': ['princeton watch wfdei',],},
                            {'texts': ['Socio Economic',],},
                            {'texts': ['Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam. Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam.',],},
                        ],
                    },
                    {
                        'cols': [
                            {'texts': ['princeton watch wfdei',],},
                            {'texts': ['Economic Socio',],},
                            {'texts': ['Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam. Sed ut perspiciatis unde omnis iste natus error sit voluptatem.',],},
                        ],
                    },
                    {
                        'invisible': True,
                        'cols': [
                            {'texts': ['princeton watch wfdei',],},
                            {'texts': ['Climate',],},
                            {'texts': ['Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam. Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam.',],},
                        ],
                    },
                    {
                        'invisible': True,
                        'cols': [
                            {'texts': ['princeton watch wfdei',],},
                            {'texts': ['Alimate 2',],},
                            {'texts': ['Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam. Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam.',],},
                        ],
                    },
                    {
                        'invisible': True,
                        'cols': [
                            {'texts': ['princeton watch wfdei',],},
                            {'texts': ['Glimac 3',],},
                            {'texts': ['Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam. Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam.',],},
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
                    {'text': 'Data Set',},
                    {'text': 'Data Type',},
                    {'text': 'Data set',},
                ],
            },
            'pagination': {
                'rowsperpage': 3,
                'numberofpages': 3,  # number of pages with current filters
                'pagenumbers': [
                    {'number': 1, 'invisible': False,},
                    {'number': 2, 'invisible': False,},
                    {'number': 3, 'invisible': False,},
                ],
                'activepage': 2,  # set to something between 1 and numberofpages
            },
            'body': {
                'rows': [
                    {
                        'invisible': True,
                        'cols': [
                            {'texts': ['princeton watch wfdei',],},
                            {'texts': ['Socio Economic',],},
                            {'texts': ['Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam. Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam.',],},
                        ],
                    },
                    {
                        'invisible': True,
                        'cols': [
                            {'texts': ['princeton watch wfdei',],},
                            {'texts': ['Economic Socio',],},
                            {'texts': ['Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam. Sed ut perspiciatis unde omnis iste natus error sit voluptatem.',],},
                        ],
                    },
                    {
                        'invisible': True,
                        'cols': [
                            {'texts': ['princeton watch wfdei',],},
                            {'texts': ['Climate F',],},
                            {'texts': ['Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam. Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam.',],},
                        ],
                    },
                    {
                        'cols': [
                            {'texts': ['princeton watch wfdei',],},
                            {'texts': ['Alimate 2 E',],},
                            {'texts': ['Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam. Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam.',],},
                        ],
                    },
                    {
                        'cols': [
                            {'texts': ['princeton watch wfdei',],},
                            {'texts': ['Glimac 3 Z',],},
                            {'texts': ['Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam. Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam.',],},
                        ],
                    },
                    {
                        'cols': [
                            {'texts': ['princeton watch wfdei',],},
                            {'texts': ['Alimate 2 W',],},
                            {'texts': ['Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam. Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam.',],},
                        ],
                    },
                    {
                        'invisible': True,
                        'cols': [
                            {'texts': ['princeton watch wfdei',],},
                            {'texts': ['Glimac 3 Q',],},
                            {'texts': ['Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam. Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam.',],},
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
                    'colnumber': '2',  # column number in table starting with 1
                    'all_value': 'All regions',
                    'name': 'region',
                    'options': [
                        {'value': 'Berlin'},
                        {'value': 'Brandenburg'},
                        {'value': 'Hamburg'},
                        {'value': 'Bremen'},
                        {'value': 'Milano'},
                        {'value': 'Venezia'},
                        {'value': 'Düsseldorf'},
                    ],
                },
                {
                    'colnumber': '3',
                    'all_value': 'All countries',
                    'name': 'country',
                    'activeoption': 'Deutschland',
                    'options': [
                        {'value': 'Deutschland'},
                        {'value': 'France'},
                        {'value': 'Italia'},
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
                    {'text': 'Town',},
                    {'text': 'Region',},
                    {'text': 'Country',},
                    {'text': 'Continent',},
                    {'text': 'Wind direction',},
                ],
            },
            'filter': '{ "3": "Deutschland" }',  # pre defined filter
            'pagination': {
                'rowsperpage': 3,
                'numberofpages': 3,  # number of pages with current filters
                'pagenumbers': [
                    {'number': 1, 'invisible': False,},
                    {'number': 2, 'invisible': False,},
                    {'number': 3, 'invisible': False,},
                    {'number': 4, 'invisible': True,},
                    {'number': 5, 'invisible': True,},
                ],
                'activepage': 1,  # set to something between 1 and numberofpages
            },
            'norowvisible': False,  # true when no row is visible
            'body': {
                'rows': [
                    {
                        'invisible': False,
                        'cols': [
                            {'texts': ['Berlin',],},
                            {'texts': ['Berlin',],},
                            {'texts': ['Deutschland',],},
                            {'texts': ['Europe',],},
                            {'texts': ['North',],},
                        ],
                    },
                    {
                        'invisible': False,
                        'cols': [
                            {'texts': ['München',],},
                            {'texts': ['Bayern',],},
                            {'texts': ['Deutschland',],},
                            {'texts': ['Europe',],},
                            {'texts': ['North West',],},
                        ],
                    },
                    {
                        'invisible': False,
                        'cols': [
                            {'texts': ['Hamburg',],},
                            {'texts': ['Hamburg',],},
                            {'texts': ['Deutschland',],},
                            {'texts': ['Europe',],},
                            {'texts': ['West',],},
                        ],
                    },
                    {
                        'invisible': True,
                        'cols': [
                            {'texts': ['Belzig',],},
                            {'texts': ['Brandenburg',],},
                            {'texts': ['Deutschland',],},
                            {'texts': ['Europe',],},
                            {'texts': ['West',],},
                        ],
                    },
                    {
                        'invisible': True,
                        'cols': [
                            {'texts': ['Atlantis',],},
                            {'texts': ['Brandenburg',],},
                            {'texts': ['Deutschland','Italia',],},
                            {'texts': ['Europe',],},
                            {'texts': ['West',],},
                        ],
                    },
                    {
                        'invisible': True,
                        'cols': [
                            {'texts': ['Wollin',],},
                            {'texts': ['Brandenburg',],},
                            {'texts': ['Deutschland',],},
                            {'texts': ['Europe',],},
                            {'texts': ['East',],},
                        ],
                    },
                    {
                        'invisible': True,
                        'cols': [
                            {'texts': ['Frankfurt Oder',],},
                            {'texts': ['Brandenburg',],},
                            {'texts': ['Deutschland',],},
                            {'texts': ['Europe',],},
                            {'texts': ['East',],},
                        ],
                    },
                    {
                        'invisible': True,
                        'cols': [
                            {'texts': ['Bremen',],},
                            {'texts': ['Bremen',],},
                            {'texts': ['Deutschland',],},
                            {'texts': ['Europe',],},
                            {'texts': ['East',],},
                        ],
                    },
                    {
                        'invisible': True,
                        'cols': [
                            {'texts': ['Bremerhaven',],},
                            {'texts': ['Bremen',],},
                            {'texts': ['Deutschland',],},
                            {'texts': ['Europe',],},
                            {'texts': ['East',],},
                        ],
                    },
                    {
                        'invisible': True,
                        'cols': [
                            {'texts': ['Paris',],},
                            {'texts': ['Paris',],},
                            {'texts': ['France',],},
                            {'texts': ['Europe',],},
                            {'texts': ['South West',],},
                        ],
                    },
                    {
                        'invisible': True,
                        'cols': [
                            {'texts': ['Milano',],},
                            {'texts': ['Milano',],},
                            {'texts': ['Italia',],},
                            {'texts': ['Europe',],},
                            {'texts': ['South',],},
                        ],
                    },
                    {
                        'invisible': True,
                        'cols': [
                            {'texts': ['Venezia',],},
                            {'texts': ['Milano',],},
                            {'texts': ['Italia',],},
                            {'texts': ['Europe',],},
                            {'texts': ['East',],},
                        ],
                    },
                    {
                        'invisible': True,
                        'cols': [
                            {'texts': ['Düsseldorf',],},
                            {'texts': ['Nordrhein-Westfalen',],},
                            {'texts': ['Deutschland',],},
                            {'texts': ['Europe',],},
                            {'texts': ['North West',],},
                        ],
                    },
                ],
            },
        },
    },


    'button_tableexport': {
        'name': 'Button for Table Export',
        'template': 'widgets/button.html',
        'context': {
            'href': '//export/table/?filter=%223%22%3A%22Deutschland%22',
            'text': 'Download Current Table',
            'tableid': 'selectortable',
        },
    },

    'expandable': {
        'name': 'Expandable',
        'template': 'widgets/expandable.html',
        'context': {
            'headline': 'FAQ for researchers',
            'editlink': '<a href="http://google.de">edit</a> | <a href="http://google.de">remove</a>',
            'list': [
                {
                    'term': 'Regular definition, closed on load',
                    'definitions': [
                        {
                            'text': 'Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque. Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque. Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque',},
                    ],
                },
                {
                    'term': 'Definitions already opened',
                    'definitions': [
                        {
                            'text': 'Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque. Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque. Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque',},
                    ],
                    'opened': True,
                },
                {
                    'definitions': [
                        {'text': 'This definition has no term.',},
                        {'text': 'This is the second definition with no term.',},
                    ],
                    'opened': True,
                    'notoggle': True,
                },
                {
                    'term': 'Term without definition',
                    'opened': True,
                    'definitions': [
                    ],
                },
            ],
        },
    },

    'expandable_light': {
        'name': 'Expandable no Headline',
        'template': 'widgets/expandable.html',
        'context': {
            'list': [
                {
                    'term': 'Regular definition, closed on load',
                    'definitions': [
                        {
                            'text': 'Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque. Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque. Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque',},
                    ],
                },
                {
                    'term': 'Definitions already opened',
                    'definitions': [
                        {
                            'text': 'Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque. Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque. Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque',},
                    ],
                    'opened': True,
                },
                {
                    'term': 'Definitions non Togglum sunt',
                    'definitions': [
                        {
                            'text': 'Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque. Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque. Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque',},
                    ],
                    'opened': True,
                    'notoggle': True,
                },
                {
                    'term': 'Multiple definitions',
                    'definitions': [
                        {
                            'text': 'Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque. Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque. Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque',},
                        {'text': 'Perspiciatis unde omnis iste.',},
                        {
                            'text': 'Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque. Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque. Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque',},
                    ],
                    'opened': True,
                    'notoggle': True,
                },
            ],
        },
    },




    'textinput': {
        'name': 'Textinput',
        'template': 'widgets/textinput.html',
        'context': {
            'id': 'textinput',
            'label': 'Name',
            'value': 'Schon ausgefüllt',
            'placeholder': 'Liesschen Müller',
        },
    },
    'textinput_helptext': {
        'name': 'Textinput with Helptext',
        'template': 'widgets/textinput.html',
        'context': {
            'id': 'textinput2',
            'label': 'Name',
            'help': 'Bitte gib hier ein, dass du einen Namen hast, und vielleicht deinen Namen.',
        },
    },
    'textinput_error': {
        'name': 'Textinput with Error',
        'template': 'widgets/textinput.html',
        'context': {
            'id': 'textinput3',
            'label': 'Name',
            'help': 'Bitte gib hier ein, dass du einen Namen hast, und vielleicht deinen Namen.',
            'error': True,
        },
    },
    'textinput_readonly': {
        'name': 'Textinput Read Only',
        'template': 'widgets/textinput.html',
        'context': {
            'id': 'textinput4',
            'label': 'Name',
            'help': 'Bitte gib hier ein, dass du einen Namen hast, und vielleicht deinen Namen.',
            'readonly': True,
        },
    },
    'textinput_email': {
        'name': 'Textinput Email',
        'template': 'widgets/textinput.html',
        'context': {
            'id': 'textinput5',
            'label': 'E-Mail',
            'type': 'email',
            'value': '',
            'placeholder': 'tester@sinnwerkstatt.com',
        },
    },

    'textarea': {
        'name': 'Textarea',
        'template': 'widgets/textarea.html',
        'context': {
            'id': 'textarea',
            'label': 'Dein Leben',
            'value': 'Schon\nausgefüllt',
            'placeholder': 'Am Anfang war das Lieschen',
        },
    },
    'textarea_error': {
        'name': 'Textarea',
        'template': 'widgets/textarea.html',
        'context': {
            'id': 'textarea2',
            'label': 'Dein Leben',
            'error': True,
            'help': 'In dieses Feld passt dein ganzes Leben.'
        },
    },

    'nullboolean': {
        'name': 'Nullboolean',
        'template': 'widgets/nullboolean.html',
        'context': {
            'id': 'nullboolean',
            'label': 'Hollywood hat alle Apollo-Missionen auf dem Mond gedreht',
            'value': True,
            'nullable': True,
        },
    },
    'nullboolean_error': {
        'name': 'Nullboolean with Error',
        'template': 'widgets/nullboolean.html',
        'context': {
            'id': 'nullboolean2',
            'label': 'Hollywood hat alle Apollo-Missionen auf dem Mond gedreht',
            'value': False,
            'error': True,
            'help': 'Ja nö oder egal?',
            'nullable': True,
        },
    },
    'nullboolean_nonull': {
        'name': 'Nullboolean not Nullable',
        'template': 'widgets/nullboolean.html',
        'context': {
            'id': 'nullboolean3',
            'label': 'Hollywood hat alle Apollo-Missionen auf dem Mond gedreht',
            'value': False,
        },
    },

    'multiselect': {
        'name': 'Multiselect',
        'template': 'widgets/multiselect.html',
        'context': {
            'id': 'multiselect',
            'label': 'Wie alt sind deine Witze?',
            'allowcustom': True,
            'options': [
                {'value':'alt', 'label':'Alt', 'checked':True},
                {'value':'neu', 'label':'Neu', 'checked':False},
                {'value':'von gestern', 'label':'Von gestern', 'checked':False},
                {'value':'neu 2016', 'label':'neu 2016', 'checked':False},
            ],
        },
    },


    'singleselect': {
        'name': 'Singleselect',
        'template': 'widgets/multiselect.html',
        'context': {
            'id': 'singleselect',
            'label': 'Von wann ist dein Longboard?',
            'singleselect': True,
            'allowcustom': True,
            'options': [
                {'value':'alt', 'label':'Alt', 'checked':False},
                {'value':'neu', 'label':'Neu', 'checked':False},
                {'value':'von gestern', 'label':'Von gestern', 'checked':False},
                {'value':'neu 2016', 'label':'neu 2016', 'checked':True},
            ],
        },
    },
    'singleselect_error': {
        'name': 'Singleselect',
        'template': 'widgets/multiselect.html',
        'context': {
            'id': 'singleselect2',
            'label': 'Von wann ist dein Longboard?',
            'singleselect': True,
            'allowcustom': True,
            'options': [
                {'value':'alt', 'label':'Alt', 'checked':False},
                {'value':'neu', 'label':'Neu', 'checked':False},
                {'value':'von gestern', 'label':'Von gestern', 'checked':False},
                {'value':'neu 2016', 'label':'neu 2016', 'checked':True},
            ],
            'error': True,
            'help': 'Hier klickste was rein.'
        },
    },

    'paper_editor_main': {
        'name': 'Paper Editor – Main Paper',
        'template': 'widgets/paper-editor.html',
        'context': {
            'id': 'papereditor',
            'label': 'Main Paper',
            'help': 'Enter the main paper of the impact model.',
            'maxpapercount': 1,
            'papers': [
                {
                    'title': 'Die Ottifanten',
                    'doi': 'DOIcodeZero',
                    'issn': '90210',
                    'date': 'Mar 2016',
                    'url': 'http://sinnwerkstatt.com',
                },
            ],
        },
    },
    'paper_editor_other': {
        'name': 'Paper Editor – Other Papers',
        'template': 'widgets/paper-editor.html',
        'context': {
            'id': 'papereditor',
            'label': 'Other Papers',
            'help': 'Enter the other papers of the impact model.',
            'maxpapercount': 5,
            'papers': [
                {
                    'title': 'Die Ottifanten',
                    'doi': 'DOIcodeZero',
                    'issn': '90210',
                    'date': 'Mar 2016',
                    'url': 'http://sinnwerkstatt.com',
                },
                {
                    'title': 'Los Simpsons',
                    'doi': 'DOIcodeZero',
                    'issn': '90210',
                    'date': 'Mar 2016',
                    'url': 'http://sinnwerkstatt.com',
                },
                {
                    'title': 'Charmed',
                    'doi': 'DOIcodeZero',
                    'issn': '90210',
                    'date': 'Mar 2016',
                    'url': 'http://sinnwerkstatt.com',
                },
            ],
        },
    },



    'twitter': {
        'name': 'Twitter',
        'template': 'widgets/twitter.html',
        'context': {
            'username': 'ISIMIPImpacts',
            'timeline': [
               {
                  "id_str":"783214",
                  "screen_name":"twitter",
                  "name":"Twitter",
                  "profile_image_url_https":"https://pbs.twimg.com/profile_images/666407537084796928/YBGgi9BO_normal.png",
                  "created_at":"Fri Apr 15 20:50:03",
                  "text":"👶 or 🍞 ?<br /><br /><a href=\"https://t.co/Mi0J3fOPWi\">https://t.co/Mi0J3fOPWi</a>"
               },
               {
                  "id_str":"783214",
                  "screen_name":"twitter",
                  "name":"Twitter",
                  "profile_image_url_https":"https://pbs.twimg.com/profile_images/666407537084796928/YBGgi9BO_normal.png",
                  "created_at":"Fri Apr 15 17:18:24",
                  "text":"Try it out — send this Tweet privately.<br /><br />✅ Tap the Message button<br />✅ Pick a pal (or a few)<br />✅ Weekend plans, done! <a href=\"https://t.co/nzzfjCJwFH\">https://t.co/nzzfjCJwFH</a>",
                  "extended_entities":{
                     "media_url_https":"https://pbs.twimg.com/tweet_video_thumb/CgGYROAVAAEl4Bi.jpg"
                  }
               },
               {
                  "id_str":"783214",
                  "screen_name":"twitter",
                  "name":"Twitter",
                  "profile_image_url_https":"https://pbs.twimg.com/profile_images/666407537084796928/YBGgi9BO_normal.png",
                  "created_at":"Fri Apr 15 17:14:14",
                  "text":"The new Message button on iOS and Android makes it easier to send Tweets privately — here's how it works 👇 <a href=\"https://t.co/UXwoRA7Pl6\">https://t.co/UXwoRA7Pl6</a>",
                  "extended_entities":{
                     "media_url_https":"https://pbs.twimg.com/tweet_video_thumb/CgGXU1DUMAAFP7P.jpg"
                  }
               },
               {
                  "id_str":"586671909",
                  "screen_name":"vine",
                  "name":"Vine",
                  "profile_image_url_https":"https://pbs.twimg.com/profile_images/694618322567053313/A5XWC_zL_normal.jpg",
                  "created_at":"Thu Apr 14 22:15:07",
                  "text":"Sharing is caring 🎾 <a href=\"https://t.co/mEJ3FOk2zX\">https://t.co/mEJ3FOk2zX</a>"
               },
               {
                  "id_str":"36771809",
                  "screen_name":"NatlParkService",
                  "name":"NationalParkService",
                  "profile_image_url_https":"https://pbs.twimg.com/profile_images/2179200522/NPS_SocialMediaProfilePic_Blue_normal.png",
                  "created_at":"Thu Apr 14 02:05:37",
                  "text":"National Park Week starts 4/16! Tweet <a href=\"https://twitter.com/search/%23FindYourPark\">#FindYourPark</a> or <a href=\"https://twitter.com/search/%23EncuentraTuParque\">#EncuentraTuParque</a> to unlock our Twitter emoji––a ranger! <a href=\"https://t.co/fp6XjJwJF1\">https://t.co/fp6XjJwJF1</a>",
                  "extended_entities":{
                     "media_url_https":"https://pbs.twimg.com/tweet_video_thumb/Cf99xcsWEAEtHrX.jpg"
                  }
               },
               {
                  "id_str":"783214",
                  "screen_name":"twitter",
                  "name":"Twitter",
                  "profile_image_url_https":"https://pbs.twimg.com/profile_images/666407537084796928/YBGgi9BO_normal.png",
                  "created_at":"Thu Apr 14 18:30:56",
                  "text":"Why did <a href=\"https://twitter.com/search/%23InkyTheOctopus\">#InkyTheOctopus</a> leave his tank at the aquarium? 🐙<br /><br /><a href=\"https://t.co/xdHLZskax3\">https://t.co/xdHLZskax3</a>"
               },
               {
                  "id_str":"1526228120",
                  "screen_name":"TwitterData",
                  "name":"Twitter Data",
                  "profile_image_url_https":"https://pbs.twimg.com/profile_images/378800000079832947/a1e83160378bce402803aefcfb07e167_normal.png",
                  "created_at":"Thu Apr 14 16:59:25",
                  "text":"The final game for <a href=\"https://twitter.com/kobebryant\">@kobebryant</a>: 60 points, 4.2 million Tweets <a href=\"https://twitter.com/search/%23ThankYouKobe\">#ThankYouKobe</a> <a href=\"https://t.co/37HnqqWBv7\">https://t.co/37HnqqWBv7</a> <a href=\"https://t.co/DoAdFCxIK1\">https://t.co/DoAdFCxIK1</a>",
                  "extended_entities":{
                     "media_url_https":"https://pbs.twimg.com/media/CgBKYbBWIAAWQW9.jpg"
                  }
               },
               {
                  "id_str":"277761722",
                  "screen_name":"TwitterUK",
                  "name":"Twitter UK",
                  "profile_image_url_https":"https://pbs.twimg.com/profile_images/2284174643/t4f37ixzn1hnfr62iw7z_normal.png",
                  "created_at":"Thu Apr 14 07:54:03",
                  "text":"Wherever you are, celebrate! Twitter is your dance floor. THIS👇 IS HAPPENING 🎉  <a href=\"https://twitter.com/search/%23KeepDancing\">#KeepDancing</a> 👯 💃🏻 <a href=\"https://t.co/EPWssqtWmz\">https://t.co/EPWssqtWmz</a>",
                  "extended_entities":{
                     "media_url_https":"https://pbs.twimg.com/ext_tw_video_thumb/720519513003986944/pu/img/bhFRv0kl0YtwrBIS.jpg"
                  }
               },
               {
                  "id_str":"586671909",
                  "screen_name":"vine",
                  "name":"Vine",
                  "profile_image_url_https":"https://pbs.twimg.com/profile_images/694618322567053313/A5XWC_zL_normal.jpg",
                  "created_at":"Wed Apr 13 20:59:02",
                  "text":"There’s an ALL NEW way to watch Vine: Hit the “Watch” button to play any channel 🍿 <a href=\"https://t.co/8PqxO01VRn\">https://t.co/8PqxO01VRn</a>"
               },
               {
                  "id_str":"783214",
                  "screen_name":"twitter",
                  "name":"Twitter",
                  "profile_image_url_https":"https://pbs.twimg.com/profile_images/666407537084796928/YBGgi9BO_normal.png",
                  "created_at":"Wed Apr 13 21:05:14",
                  "text":"From helpful to hilarious, explore the automated world of Twitter bots 🤖<br /><br /><a href=\"https://t.co/ldPZPSHvw5\">https://t.co/ldPZPSHvw5</a>"
               },
               {
                  "id_str":"972651",
                  "screen_name":"mashable",
                  "name":"Mashable",
                  "profile_image_url_https":"https://pbs.twimg.com/profile_images/672144573725044737/eEOLvMTQ_normal.png",
                  "created_at":"Wed Apr 13 13:31:31",
                  "text":"The story of Kobe Bryant's epic career, as told by his 10 most popular tweets: <a href=\"https://t.co/cvlkdFBvTK\">https://t.co/cvlkdFBvTK</a> <a href=\"https://t.co/0meTgCArU9\">https://t.co/0meTgCArU9</a>",
                  "extended_entities":{
                     "media_url_https":"https://pbs.twimg.com/media/Cf7RNS9UUAAgnLo.jpg"
                  }
               },
               {
                  "id_str":"783214",
                  "screen_name":"twitter",
                  "name":"Twitter",
                  "profile_image_url_https":"https://pbs.twimg.com/profile_images/666407537084796928/YBGgi9BO_normal.png",
                  "created_at":"Wed Apr 13 16:30:13",
                  "text":"Group Direct Messages keep those who need to know, in the know. <br /><br />Party with <a href=\"https://twitter.com/search/%23TwitterTips\">#TwitterTips</a> 🎉 <a href=\"https://t.co/JMBg3mMb7k\">https://t.co/JMBg3mMb7k</a><br /><a href=\"https://t.co/wF6bJhm9yM\">https://t.co/wF6bJhm9yM</a>"
               },
               {
                  "id_str":"783214",
                  "screen_name":"twitter",
                  "name":"Twitter",
                  "profile_image_url_https":"https://pbs.twimg.com/profile_images/666407537084796928/YBGgi9BO_normal.png",
                  "created_at":"Tue Apr 12 19:10:07",
                  "text":"For <a href=\"https://twitter.com/search/%23TravelTuesday\">#TravelTuesday</a> 🏔 views and 🐬 visits, coast to Kaikoura, New Zealand.<br /><a href=\"https://t.co/cEtNchNmzF\">https://t.co/cEtNchNmzF</a>"
               },
               {
                  "id_str":"1347713256",
                  "screen_name":"TwitterCanada",
                  "name":"Twitter Canada",
                  "profile_image_url_https":"https://pbs.twimg.com/profile_images/649613056956215296/e_4DZvlc_normal.png",
                  "created_at":"Tue Apr 12 14:02:42",
                  "text":"It's official: Moments has arrived in 🇨🇦, a new way to experience the best of Twitter <a href=\"https://t.co/t0mxxPdloF\">https://t.co/t0mxxPdloF</a> <a href=\"https://t.co/m46KONi07z\">https://t.co/m46KONi07z</a>",
                  "extended_entities":{
                     "media_url_https":"https://pbs.twimg.com/tweet_video_thumb/Cf2NAqIUUAAyICM.jpg"
                  }
               },
               {
                  "id_str":"783214",
                  "screen_name":"twitter",
                  "name":"Twitter",
                  "profile_image_url_https":"https://pbs.twimg.com/profile_images/666407537084796928/YBGgi9BO_normal.png",
                  "created_at":"Tue Apr 12 13:25:46",
                  "text":"Hear that? Turn up the volume for <a href=\"https://twitter.com/Stereogum\">@Stereogum</a>'s favorite new music, powered by <a href=\"https://twitter.com/SoundCloud\">@SoundCloud</a> 🎧 <a href=\"https://t.co/JVtZHMyZ4A\">https://t.co/JVtZHMyZ4A</a>"
               },
               {
                  "id_str":"783214",
                  "screen_name":"twitter",
                  "name":"Twitter",
                  "profile_image_url_https":"https://pbs.twimg.com/profile_images/666407537084796928/YBGgi9BO_normal.png",
                  "created_at":"Mon Apr 11 17:55:19",
                  "text":"Best friends come in many sizes <a href=\"https://twitter.com/search/%23NationalPetDay\">#NationalPetDay</a> 🐶<br /><a href=\"https://t.co/Mryb3vJWPS\">https://t.co/Mryb3vJWPS</a><br /><a href=\"https://t.co/A2D6cnGCOu\">https://t.co/A2D6cnGCOu</a>"
               },
               {
                  "id_str":"3015271772",
                  "screen_name":"TwitterFood",
                  "name":"Twitter Food",
                  "profile_image_url_https":"https://pbs.twimg.com/profile_images/593168479978659843/dl3IaBJh_normal.jpg",
                  "created_at":"Mon Apr 11 11:28:25",
                  "text":"️☕️ <a href=\"https://twitter.com/search/%23MotivationMonday\">#MotivationMonday</a>, coffee edition: <a href=\"https://twitter.com/tastemade\">@tastemade</a> shows you all the ways to drink it, bake it, and even grill it👇<br /><br /><a href=\"https://t.co/kCpkMPnAzH\">https://t.co/kCpkMPnAzH</a>"
               },
               {
                  "id_str":"783214",
                  "screen_name":"twitter",
                  "name":"Twitter",
                  "profile_image_url_https":"https://pbs.twimg.com/profile_images/666407537084796928/YBGgi9BO_normal.png",
                  "created_at":"Sat Apr 09 17:15:46",
                  "text":"Spring through Saturday with cherry blossom videos from around Japan 🌸 <a href=\"https://t.co/2QZWILEtzG\">https://t.co/2QZWILEtzG</a>",
                  "quoted_status":{
                     "text":"🌸もうお花見をされた方も、これからの方も、今年はお花見なしの方も、Twitter上の各地からの #桜 の動画もお見逃しなく。たくさんの動画ツイートから、ごく一部を集めました。🌸<br /><a href=\"https://t.co/XdLBBwMNVR\">https://t.co/XdLBBwMNVR</a> <a href=\"https://t.co/uC0Y7jQTmH\">https://t.co/uC0Y7jQTmH</a>",
                     "media_url_https":"https://pbs.twimg.com/media/CfgnGURXIAABg6K.jpg"
                  }
               },
               {
                  "id_str":"783214",
                  "screen_name":"twitter",
                  "name":"Twitter",
                  "profile_image_url_https":"https://pbs.twimg.com/profile_images/666407537084796928/YBGgi9BO_normal.png",
                  "created_at":"Fri Apr 08 22:00:10",
                  "text":"From liftoff to landing, see how <a href=\"https://twitter.com/SpaceX\">@SpaceX</a> kicked off a very special delivery 🚀 <a href=\"https://t.co/3uqwKPzNFy\">https://t.co/3uqwKPzNFy</a>"
               },
               {
                  "id_str":"783214",
                  "screen_name":"twitter",
                  "name":"Twitter",
                  "profile_image_url_https":"https://pbs.twimg.com/profile_images/666407537084796928/YBGgi9BO_normal.png",
                  "created_at":"Fri Apr 08 06:15:43",
                  "text":"Calling all cricket fans! Ahead of <a href=\"https://twitter.com/search/%23IPL\">#IPL</a>, relive how the <a href=\"https://twitter.com/ICC\">@ICC</a> <a href=\"https://twitter.com/search/%23WT20\">#WT20</a> played out on Twitter: <a href=\"https://t.co/HfGoecMwtS\">https://t.co/HfGoecMwtS</a> <a href=\"https://t.co/IUju0RzqYO\">https://t.co/IUju0RzqYO</a>",
                  "extended_entities":{
                     "media_url_https":"https://pbs.twimg.com/media/Cff9g0nW8AEpMN5.png"
                  }
               },
               {
                  "id_str":"783214",
                  "screen_name":"twitter",
                  "name":"Twitter",
                  "profile_image_url_https":"https://pbs.twimg.com/profile_images/666407537084796928/YBGgi9BO_normal.png",
                  "created_at":"Thu Apr 07 22:00:17",
                  "text":"Stop, collaborate, and listen — jam out to this week's <a href=\"https://twitter.com/Vine\">@Vine</a> <a href=\"https://twitter.com/search/%23SongCollab\">#SongCollab</a> with <a href=\"https://twitter.com/witified\">@witified</a> 🎼 <a href=\"https://t.co/2jv7wNKsK7\">https://t.co/2jv7wNKsK7</a> <a href=\"https://t.co/gIHzl7kr1g\">https://t.co/gIHzl7kr1g</a>"
               },
               {
                  "id_str":"783214",
                  "screen_name":"twitter",
                  "name":"Twitter",
                  "profile_image_url_https":"https://pbs.twimg.com/profile_images/666407537084796928/YBGgi9BO_normal.png",
                  "created_at":"Thu Apr 07 19:00:41",
                  "text":"How would your Tweets look in watercolor? 🎨 <a href=\"https://t.co/M0QxKBfM3A\">https://t.co/M0QxKBfM3A</a>"
               },
               {
                  "id_str":"586671909",
                  "screen_name":"vine",
                  "name":"Vine",
                  "profile_image_url_https":"https://pbs.twimg.com/profile_images/694618322567053313/A5XWC_zL_normal.jpg",
                  "created_at":"Wed Apr 06 19:45:11",
                  "text":"🍂❄️🌷☀️ More Anime: <a href=\"https://t.co/oROmiwzwsL\">https://t.co/oROmiwzwsL</a> <br /><a href=\"https://t.co/hVATcVjSGB\">https://t.co/hVATcVjSGB</a>"
               },
               {
                  "id_str":"14199378",
                  "screen_name":"smithsonian",
                  "name":"Smithsonian",
                  "profile_image_url_https":"https://pbs.twimg.com/profile_images/3481246370/466b650a1da1c9eafaadf9f3dccaa7a8_normal.png",
                  "created_at":"Wed Apr 06 15:48:31",
                  "text":"We've done lots of Twitter tours of our many museums' collections. See them all: <a href=\"https://t.co/84c7fXvZzh\">https://t.co/84c7fXvZzh</a> <a href=\"https://t.co/ldGiA44JsT\">https://t.co/ldGiA44JsT</a>",
                  "quoted_status":{
                     "text":"Inside the vast archives of the Smithsonian’s Museum of Natural History <a href=\"https://t.co/FvuOHJeenP\">https://t.co/FvuOHJeenP</a> <a href=\"https://t.co/AzfQxm4WcO\">https://t.co/AzfQxm4WcO</a>",
                     "media_url_https":"https://pbs.twimg.com/media/CfXiZ_bW8AIiJpo.jpg"
                  }
               },
               {
                  "id_str":"783214",
                  "screen_name":"twitter",
                  "name":"Twitter",
                  "profile_image_url_https":"https://pbs.twimg.com/profile_images/666407537084796928/YBGgi9BO_normal.png",
                  "created_at":"Wed Apr 06 18:45:15",
                  "text":"We start, you finish with a friend. Fill in the blank when you send this privately with the new Message button. <a href=\"https://t.co/iYXa6zqYGV\">https://t.co/iYXa6zqYGV</a>",
                  "extended_entities":{
                     "media_url_https":"https://pbs.twimg.com/tweet_video_thumb/CfYUTXtUEAA9PhM.jpg"
                  }
               },
               {
                  "id_str":"783214",
                  "screen_name":"twitter",
                  "name":"Twitter",
                  "profile_image_url_https":"https://pbs.twimg.com/profile_images/666407537084796928/YBGgi9BO_normal.png",
                  "created_at":"Wed Apr 06 16:30:37",
                  "text":"Hear it first. Get notifications when your favorite accounts Tweet. <a href=\"https://twitter.com/search/%23TwitterTips\">#TwitterTips</a><br /><br />Learn how: <a href=\"https://t.co/cARY5wt2VT\">https://t.co/cARY5wt2VT</a><br /><a href=\"https://t.co/W3ezNsLDnf\">https://t.co/W3ezNsLDnf</a>"
               },
               {
                  "id_str":"3085835595",
                  "screen_name":"periscopetv",
                  "name":"Periscope TV",
                  "profile_image_url_https":"https://pbs.twimg.com/profile_images/581142098943983616/-Ww_5fZp_normal.png",
                  "created_at":"Tue Apr 05 22:51:58",
                  "text":"A stunning view of 🌸-covered mountains by <a href=\"https://twitter.com/DaveInOsaka\">@DaveInOsaka</a> <br /><br /><a href=\"https://t.co/Mtp03gYusg\">https://t.co/Mtp03gYusg</a> <a href=\"https://t.co/0b2eN95ayt\">https://t.co/0b2eN95ayt</a>",
                  "extended_entities":{
                     "media_url_https":"https://pbs.twimg.com/media/CfUEwlCUYAM6-GU.jpg"
                  }
               },
               {
                  "id_str":"783214",
                  "screen_name":"twitter",
                  "name":"Twitter",
                  "profile_image_url_https":"https://pbs.twimg.com/profile_images/666407537084796928/YBGgi9BO_normal.png",
                  "created_at":"Tue Apr 05 19:15:09",
                  "text":"Explore highlights from <a href=\"https://twitter.com/search/%23MuseumWeek\">#MuseumWeek</a>'s global celebration of art and culture with <a href=\"https://twitter.com/TwitterFrance\">@TwitterFrance</a> 🇫🇷 <a href=\"https://t.co/RY6M6naVw8\">https://t.co/RY6M6naVw8</a>"
               },
               {
                  "id_str":"783214",
                  "screen_name":"twitter",
                  "name":"Twitter",
                  "profile_image_url_https":"https://pbs.twimg.com/profile_images/666407537084796928/YBGgi9BO_normal.png",
                  "created_at":"Tue Apr 05 16:32:36",
                  "text":"The new Message button makes it even easier to send Tweets privately to friends: <a href=\"https://t.co/S3LMsTqW9l\">https://t.co/S3LMsTqW9l</a> <a href=\"https://t.co/HEdCxSn9RA\">https://t.co/HEdCxSn9RA</a>",
                  "extended_entities":{
                     "media_url_https":"https://pbs.twimg.com/tweet_video_thumb/CfSsw8xUEAA21fb.jpg"
                  }
               },
               {
                  "id_str":"783214",
                  "screen_name":"twitter",
                  "name":"Twitter",
                  "profile_image_url_https":"https://pbs.twimg.com/profile_images/666407537084796928/YBGgi9BO_normal.png",
                  "created_at":"Tue Apr 05 00:55:03",
                  "text":"Follow every play of the <a href=\"https://twitter.com/search/%23NationalChampionship\">#NationalChampionship</a> as <a href=\"https://twitter.com/NovaMBB\">@NovaMBB</a> and <a href=\"https://twitter.com/UNC_Basketball\">@UNC_Basketball</a> take the court. <a href=\"https://twitter.com/search/%23MarchMadness\">#MarchMadness</a> <a href=\"https://t.co/3F9I27QX3V\">https://t.co/3F9I27QX3V</a>"
               },
               {
                  "id_str":"586671909",
                  "screen_name":"vine",
                  "name":"Vine",
                  "profile_image_url_https":"https://pbs.twimg.com/profile_images/694618322567053313/A5XWC_zL_normal.jpg",
                  "created_at":"Mon Apr 04 18:26:06",
                  "text":"Vine's first art exhibit 🎥 Now in Explore: <a href=\"https://t.co/YSrykwvigx\">https://t.co/YSrykwvigx</a> <a href=\"https://t.co/CxlsBFQJR9\">https://t.co/CxlsBFQJR9</a>"
               },
               {
                  "id_str":"2535545544",
                  "screen_name":"Bitmoji",
                  "name":"Bitmoji",
                  "profile_image_url_https":"https://pbs.twimg.com/profile_images/623949592816553984/xYbD17ai_normal.png",
                  "created_at":"Mon Apr 04 19:23:11",
                  "text":"You can now copy and paste from Bitmoji Keyboard into a Tweet on iOS! To help us celebrate, Tweet this new bitmoji <a href=\"https://t.co/n7wtL5cfO9\">https://t.co/n7wtL5cfO9</a>",
                  "extended_entities":{
                     "media_url_https":"https://pbs.twimg.com/media/CfOLY60WsAA2hrH.jpg"
                  }
               },
               {
                  "id_str":"2375566652",
                  "screen_name":"MuseumWeek",
                  "name":"MuseumWeek",
                  "profile_image_url_https":"https://pbs.twimg.com/profile_images/562944735896039424/cTEyhaog_normal.png",
                  "created_at":"Fri Apr 01 17:23:11",
                  "text":"The <a href=\"https://twitter.com/search/%23FutureMW\">#FutureMW</a> looks great! <br />Get a glimpse of the future of culture here &gt; <a href=\"https://t.co/hL5EaAFZ9P\">https://t.co/hL5EaAFZ9P</a> <a href=\"https://t.co/yK24pB42YA\">https://t.co/yK24pB42YA</a>",
                  "extended_entities":{
                     "media_url_https":"https://pbs.twimg.com/media/Ce-TJlsXIAEDY9t.jpg"
                  }
               },
               {
                  "id_str":"783214",
                  "screen_name":"twitter",
                  "name":"Twitter",
                  "profile_image_url_https":"https://pbs.twimg.com/profile_images/666407537084796928/YBGgi9BO_normal.png",
                  "created_at":"Fri Apr 01 17:00:09",
                  "text":"On <a href=\"https://twitter.com/search/%23AprilFools\">#AprilFools</a> Day, are you ..."
               },
               {
                  "id_str":"1526228120",
                  "screen_name":"TwitterData",
                  "name":"Twitter Data",
                  "profile_image_url_https":"https://pbs.twimg.com/profile_images/378800000079832947/a1e83160378bce402803aefcfb07e167_normal.png",
                  "created_at":"Fri Apr 01 15:06:29",
                  "text":"Where will you find fans of each of the <a href=\"https://twitter.com/search/%23FinalFour\">#FinalFour</a> teams? Check out our map &amp; see who your town is talking about. <a href=\"https://t.co/uw3tHi71yf\">https://t.co/uw3tHi71yf</a>",
                  "extended_entities":{
                     "media_url_https":"https://pbs.twimg.com/media/Ce9z3SgWsAAR_hb.jpg"
                  }
               },
               {
                  "id_str":"3085835595",
                  "screen_name":"periscopetv",
                  "name":"Periscope TV",
                  "profile_image_url_https":"https://pbs.twimg.com/profile_images/581142098943983616/-Ww_5fZp_normal.png",
                  "created_at":"Thu Mar 31 18:24:35",
                  "text":"Travel back in time with <a href=\"https://t.co/ONbRW7ykhB\">https://t.co/ONbRW7ykhB</a> for <a href=\"https://twitter.com/search/%23MuseumWeek\">#MuseumWeek</a> <a href=\"https://t.co/7wsOFY2yJ2\">https://t.co/7wsOFY2yJ2</a>",
                  "extended_entities":{
                     "media_url_https":"https://pbs.twimg.com/media/Ce5XnhkUYAA2tQE.jpg"
                  }
               },
               {
                  "id_str":"300392950",
                  "screen_name":"TwitterSports",
                  "name":"Twitter Sports",
                  "profile_image_url_https":"https://pbs.twimg.com/profile_images/695709873917431809/N997_JOB_normal.png",
                  "created_at":"Thu Mar 31 16:25:56",
                  "text":"Play ball with <a href=\"https://twitter.com/MLB\">@MLB</a> this season on Twitter. <a href=\"https://twitter.com/search/%23CapsOn\">#CapsOn</a> <a href=\"https://t.co/IXUqBbeDEo\">https://t.co/IXUqBbeDEo</a> <a href=\"https://t.co/BgDnOtfPML\">https://t.co/BgDnOtfPML</a>",
                  "extended_entities":{
                     "media_url_https":"https://pbs.twimg.com/media/Ce48dYGVIAAyf4L.jpg"
                  }
               },
               {
                  "id_str":"783214",
                  "screen_name":"twitter",
                  "name":"Twitter",
                  "profile_image_url_https":"https://pbs.twimg.com/profile_images/666407537084796928/YBGgi9BO_normal.png",
                  "created_at":"Wed Mar 30 16:55:13",
                  "text":"Put a twist on your next Tweet — add a GIF for some extra flair.<br /><br />Want more <a href=\"https://twitter.com/search/%23TwitterTips\">#TwitterTips</a>? <a href=\"https://t.co/JMBg3mMb7k\">https://t.co/JMBg3mMb7k</a><br /><a href=\"https://t.co/PspfOmdjhq\">https://t.co/PspfOmdjhq</a>"
               },
               {
                  "id_str":"586671909",
                  "screen_name":"vine",
                  "name":"Vine",
                  "profile_image_url_https":"https://pbs.twimg.com/profile_images/694618322567053313/A5XWC_zL_normal.jpg",
                  "created_at":"Tue Mar 29 21:35:34",
                  "text":"🔵⚪️🔴 <a href=\"https://twitter.com/search/%23MuseumWeek\">#MuseumWeek</a> <a href=\"https://t.co/p3GKI95njw\">https://t.co/p3GKI95njw</a>"
               },
               {
                  "id_str":"783214",
                  "screen_name":"twitter",
                  "name":"Twitter",
                  "profile_image_url_https":"https://pbs.twimg.com/profile_images/666407537084796928/YBGgi9BO_normal.png",
                  "created_at":"Tue Mar 29 19:15:19",
                  "text":"Brace yourself, <a href=\"https://twitter.com/search/%23TravelTuesday\">#TravelTuesday</a> has come to Dubrovnik. <a href=\"https://t.co/xlvTRhSjU5\">https://t.co/xlvTRhSjU5</a>"
               },
               {
                  "id_str":"783214",
                  "screen_name":"twitter",
                  "name":"Twitter",
                  "profile_image_url_https":"https://pbs.twimg.com/profile_images/666407537084796928/YBGgi9BO_normal.png",
                  "created_at":"Tue Mar 29 14:55:21",
                  "text":"Starting today, anyone can make Tweets with images accessible to the visually impaired: <a href=\"https://t.co/mAnehClSNR\">https://t.co/mAnehClSNR</a> <a href=\"https://t.co/bmCuMVWJrR\">https://t.co/bmCuMVWJrR</a>",
                  "extended_entities":{
                     "media_url_https":"https://pbs.twimg.com/media/CeuUidaWwAAgy_5.jpg"
                  }
               },
               {
                  "id_str":"783214",
                  "screen_name":"twitter",
                  "name":"Twitter",
                  "profile_image_url_https":"https://pbs.twimg.com/profile_images/666407537084796928/YBGgi9BO_normal.png",
                  "created_at":"Mon Mar 28 22:15:26",
                  "text":"To kick off <a href=\"https://twitter.com/search/%23MuseumWeek\">#MuseumWeek</a>, discover museums' most well-kept secrets: <a href=\"https://t.co/I0IyK5xC7m\">https://t.co/I0IyK5xC7m</a><br /><br /><a href=\"https://t.co/WMudOa5BWk\">https://t.co/WMudOa5BWk</a>"
               },
               {
                  "id_str":"2445809510",
                  "screen_name":"periscopeco",
                  "name":"Periscope",
                  "profile_image_url_https":"https://pbs.twimg.com/profile_images/576529332580982785/pfta069p_normal.png",
                  "created_at":"Mon Mar 28 14:36:54",
                  "text":"Year One 📈 <a href=\"https://t.co/fb1IhwDJTK\">https://t.co/fb1IhwDJTK</a>"
               },
               {
                  "id_str":"783214",
                  "screen_name":"twitter",
                  "name":"Twitter",
                  "profile_image_url_https":"https://pbs.twimg.com/profile_images/666407537084796928/YBGgi9BO_normal.png",
                  "created_at":"Sun Mar 27 21:00:05",
                  "text":"<a href=\"https://twitter.com/search/%23MuseumWeek\">#MuseumWeek</a> is back! Join 3,000+ cultural institutions for a celebration of art and culture: <a href=\"https://t.co/NWfTAFieOL\">https://t.co/NWfTAFieOL</a> <a href=\"https://t.co/B3ziwM3kJ0\">https://t.co/B3ziwM3kJ0</a>",
                  "extended_entities":{
                     "media_url_https":"https://pbs.twimg.com/media/CelU2aLWAAAq375.jpg"
                  }
               },
               {
                  "id_str":"3015271772",
                  "screen_name":"TwitterFood",
                  "name":"Twitter Food",
                  "profile_image_url_https":"https://pbs.twimg.com/profile_images/593168479978659843/dl3IaBJh_normal.jpg",
                  "created_at":"Sat Mar 26 14:55:12",
                  "text":"️A dozen ideas for an egg-tastic <a href=\"https://twitter.com/search/%23EasterWeekend\">#EasterWeekend</a> via <a href=\"https://twitter.com/tastemade\">@tastemade</a> ⚡ <a href=\"https://t.co/IfdXTnCEqb\">https://t.co/IfdXTnCEqb</a>"
               },
               {
                  "id_str":"3085835595",
                  "screen_name":"periscopetv",
                  "name":"Periscope TV",
                  "profile_image_url_https":"https://pbs.twimg.com/profile_images/581142098943983616/-Ww_5fZp_normal.png",
                  "created_at":"Fri Mar 25 18:46:38",
                  "text":"Periscope's first birthday is tomorrow! Help us start celebrating by broadcasting with <a href=\"https://twitter.com/search/%23YearOne\">#YearOne</a> 🎉🎈 <a href=\"https://t.co/kGiKroWV6q\">https://t.co/kGiKroWV6q</a>",
                  "extended_entities":{
                     "media_url_https":"https://pbs.twimg.com/media/CeajICjUEAAgu4l.jpg"
                  }
               },
               {
                  "id_str":"783214",
                  "screen_name":"twitter",
                  "name":"Twitter",
                  "profile_image_url_https":"https://pbs.twimg.com/profile_images/666407537084796928/YBGgi9BO_normal.png",
                  "created_at":"Fri Mar 25 19:00:12",
                  "text":"What would you try in zero gravity? 🚀 <a href=\"https://t.co/4QWs39xeaU\">https://t.co/4QWs39xeaU</a>"
               },
               {
                  "id_str":"783214",
                  "screen_name":"twitter",
                  "name":"Twitter",
                  "profile_image_url_https":"https://pbs.twimg.com/profile_images/666407537084796928/YBGgi9BO_normal.png",
                  "created_at":"Thu Mar 24 23:45:10",
                  "text":"😄😃😀😊☺😉😍😘😚😗😙😜😝😛😳😁😔😌😒😞😣<br />😢😂😭😪😥😰😅😓😩😫😨😱😠😡😤😖😆😋😷😎😴<br />😵😲😟😦😧😈👿😮😬😐😕😯😶😇😏😑👲👳👮👷💂<br />👶👦👧👨👩👴👵👱👼👸😺😸😻😽😼🙀😿😹😾👹👺<br />🙈🙉🙊💀👽💩🔥✨🌟💫💥💢💦💧💤💨👂👀👃👅👄<br />👍👎👌👊✊✌👋✋👐👆👇👉👈🙌🙏☝👏💪🚶🏃💃<br />👫👪👬👭💏💑👯🙆🙅💁🙋💆💇💅👰🙎🙍🙇🎩👑👒<br />👟👞👡👠👢👕👔👚👗🎽👖👘👙💼👜👝👛👓🎀🌂💄<br />💛💙💜💚❤💔💗💓💕💖💞💘💌💋💍💎👤👥💬👣💭"
               },
               {
                  "id_str":"3085835595",
                  "screen_name":"periscopetv",
                  "name":"Periscope TV",
                  "profile_image_url_https":"https://pbs.twimg.com/profile_images/581142098943983616/-Ww_5fZp_normal.png",
                  "created_at":"Thu Mar 24 21:51:47",
                  "text":"🐶🐺🐱🐭🐹🐰🐸🐯🐨🐻🐷🐽🐮🐗🐵🐒🐴🐑🐘🐼🐧<br />🐦🐤🐥🐣🐔🐍🐢🐛🐝🐜🐞🐌🐙🐚🐠🐟🐬🐳🐋🐄🐏<br />🐀🐃🐅🐇🐉🐎🐐🐓🐕🐖🐁🐂🐲🐡🐊🐫🐪🐆🐈🐩🐾<br />💐🌸🌷🍀🌹🌻🌺🍁🍃🍂🌿🌾🍄🌵🌴🌲🌳🌰🌱🌼🌐<br />🌞🌝🌚🌑🌒🌓🌔🌕🌜🌛🌙🌍🌎🌏🌋🌌🌠⭐<br />☀⛅☁⚡☔❄⛄🌀🌁🌈🌊💩",
                  "extended_entities":{
                     "media_url_https":"https://pbs.twimg.com/media/CeWD6aNUkAAqnxJ.jpg"
                  }
               },
               {
                  "id_str":"103770785",
                  "screen_name":"TwitterIndia",
                  "name":"Twitter India",
                  "profile_image_url_https":"https://pbs.twimg.com/profile_images/2284174752/64pe9ctjko2omrtcij7a_normal.png",
                  "created_at":"Thu Mar 24 17:46:30",
                  "text":"🏠🏡🏫🏢🏣🏥🏦🏪🏩🏨💒⛪🏬🏤🌇🌆🏯🏰⛺🏭🗼<br />🗾🗻🌄🌅🌃🗽🌉🎠🎡⛲🎢🚢⛵🚤🚣⚓🚀✈💺🚁🚂<br />🚊🚉🚎🚆🚄🚅🚈🚇🚝🚋🚃🚎🚌🚍🚙🚘🚗🚕🚖🚛🚚<br />🚨🚓🚔🚒🚑🚐🚲🚡🚟🚠🚜💈🚏🎫🚦🚥⚠🚧🔰⛽🏮<br />🎰♨🗿🎪🎭📍🚩🇯🇵🇰🇷🇩🇪🇨🇳🇺🇸🇫🇷🇪🇸🇮🇹🇷🇺🇬🇧"
               },
            ],
        },
    },



    'twitter_empty': {
        'name': 'Twitter Empty',
        'template': 'widgets/twitter.html',
        'context': {
            'username': 'ISIMIPImpacts',
            'timeline': False,
        },
    },



    'footer': {
        'name': 'Footer',
        'template': 'widgets/footer.html',
        'context': {
            'links': [
                {'url': 'http://google.de', 'text': 'Kontakt'},
                {'url': 'http://bing.de', 'text': 'Presse', 'active': True},
                {'url': 'http://google.de', 'text': 'Newsletter'},
            ],
        },
    },

}
