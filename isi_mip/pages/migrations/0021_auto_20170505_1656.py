# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-05-05 14:56
from __future__ import unicode_literals

from django.db import migrations
import isi_mip.contrib.blocks
import isi_mip.pages.blocks
import wagtail.contrib.table_block.blocks
import wagtail.wagtailcore.blocks
import wagtail.wagtailcore.fields
import wagtail.wagtaildocs.blocks
import wagtail.wagtailembeds.blocks
import wagtail.wagtailimages.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0020_homepage_show_toc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aboutpage',
            name='content',
            field=wagtail.wagtailcore.fields.StreamField((('heading', isi_mip.contrib.blocks.HeadingBlock()), ('rich_text', isi_mip.contrib.blocks.RichTextBlock()), ('horizontal_ruler', wagtail.wagtailcore.blocks.StreamBlock(())), ('embed', wagtail.wagtailembeds.blocks.EmbedBlock()), ('image', isi_mip.contrib.blocks.ImageBlock()), ('table', wagtail.contrib.table_block.blocks.TableBlock()), ('monospace_text', isi_mip.contrib.blocks.MonospaceTextBlock()), ('columns_1_to_1', wagtail.wagtailcore.blocks.StructBlock((('left_column', wagtail.wagtailcore.blocks.StreamBlock((('heading', isi_mip.contrib.blocks.HeadingBlock()), ('rich_text', isi_mip.contrib.blocks.RichTextBlock()), ('horizontal_ruler', wagtail.wagtailcore.blocks.StreamBlock(())), ('embed', wagtail.wagtailembeds.blocks.EmbedBlock()), ('image', isi_mip.contrib.blocks.ImageBlock()), ('table', wagtail.contrib.table_block.blocks.TableBlock()), ('monospace_text', isi_mip.contrib.blocks.MonospaceTextBlock()), ('small_teaser', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock(required=True)), ('picture', wagtail.wagtailimages.blocks.ImageChooserBlock()), ('text', wagtail.wagtailcore.blocks.TextBlock(required=True)), ('link', wagtail.wagtailcore.blocks.PageChooserBlock(required=True))))), ('big_teaser', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock(required=True)), ('subtitle', wagtail.wagtailcore.blocks.CharBlock(required=False)), ('picture', wagtail.wagtailimages.blocks.ImageChooserBlock()), ('text', isi_mip.contrib.blocks.RichTextBlock()), ('external_link', wagtail.wagtailcore.blocks.URLBlock(help_text='Will be ignored if an internal link is provided', required=False)), ('internal_link', wagtail.wagtailcore.blocks.PageChooserBlock(help_text='If set, this has precedence over the external link.', required=False)), ('from_date', wagtail.wagtailcore.blocks.DateBlock(required=False)), ('to_date', wagtail.wagtailcore.blocks.DateBlock(required=False))))), ('isinumbers', wagtail.wagtailcore.blocks.StructBlock((('number1', wagtail.wagtailcore.blocks.StructBlock((('number', wagtail.wagtailcore.blocks.CharBlock()), ('title', wagtail.wagtailcore.blocks.CharBlock()), ('text', wagtail.wagtailcore.blocks.CharBlock())))), ('number2', wagtail.wagtailcore.blocks.StructBlock((('number', wagtail.wagtailcore.blocks.CharBlock()), ('title', wagtail.wagtailcore.blocks.CharBlock()), ('text', wagtail.wagtailcore.blocks.CharBlock()))))))), ('link', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock(required=True)), ('picture', wagtail.wagtailimages.blocks.ImageChooserBlock(required=False)), ('text', isi_mip.contrib.blocks.RichTextBlock(required=False)), ('link', wagtail.wagtailcore.blocks.URLBlock(required=False)), ('date', wagtail.wagtailcore.blocks.DateBlock(required=False))))), ('faqs', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock()), ('faqs', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock((('question', wagtail.wagtailcore.blocks.CharBlock()), ('answer', isi_mip.contrib.blocks.RichTextBlock())))))))), ('pdf', wagtail.wagtailcore.blocks.StructBlock((('file', wagtail.wagtaildocs.blocks.DocumentChooserBlock()), ('description', wagtail.wagtailcore.blocks.CharBlock()))))))), ('right_column', wagtail.wagtailcore.blocks.StreamBlock((('heading', isi_mip.contrib.blocks.HeadingBlock()), ('rich_text', isi_mip.contrib.blocks.RichTextBlock()), ('horizontal_ruler', wagtail.wagtailcore.blocks.StreamBlock(())), ('embed', wagtail.wagtailembeds.blocks.EmbedBlock()), ('image', isi_mip.contrib.blocks.ImageBlock()), ('table', wagtail.contrib.table_block.blocks.TableBlock()), ('monospace_text', isi_mip.contrib.blocks.MonospaceTextBlock()), ('small_teaser', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock(required=True)), ('picture', wagtail.wagtailimages.blocks.ImageChooserBlock()), ('text', wagtail.wagtailcore.blocks.TextBlock(required=True)), ('link', wagtail.wagtailcore.blocks.PageChooserBlock(required=True))))), ('big_teaser', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock(required=True)), ('subtitle', wagtail.wagtailcore.blocks.CharBlock(required=False)), ('picture', wagtail.wagtailimages.blocks.ImageChooserBlock()), ('text', isi_mip.contrib.blocks.RichTextBlock()), ('external_link', wagtail.wagtailcore.blocks.URLBlock(help_text='Will be ignored if an internal link is provided', required=False)), ('internal_link', wagtail.wagtailcore.blocks.PageChooserBlock(help_text='If set, this has precedence over the external link.', required=False)), ('from_date', wagtail.wagtailcore.blocks.DateBlock(required=False)), ('to_date', wagtail.wagtailcore.blocks.DateBlock(required=False))))), ('isinumbers', wagtail.wagtailcore.blocks.StructBlock((('number1', wagtail.wagtailcore.blocks.StructBlock((('number', wagtail.wagtailcore.blocks.CharBlock()), ('title', wagtail.wagtailcore.blocks.CharBlock()), ('text', wagtail.wagtailcore.blocks.CharBlock())))), ('number2', wagtail.wagtailcore.blocks.StructBlock((('number', wagtail.wagtailcore.blocks.CharBlock()), ('title', wagtail.wagtailcore.blocks.CharBlock()), ('text', wagtail.wagtailcore.blocks.CharBlock()))))))), ('link', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock(required=True)), ('picture', wagtail.wagtailimages.blocks.ImageChooserBlock(required=False)), ('text', isi_mip.contrib.blocks.RichTextBlock(required=False)), ('link', wagtail.wagtailcore.blocks.URLBlock(required=False)), ('date', wagtail.wagtailcore.blocks.DateBlock(required=False))))), ('faqs', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock()), ('faqs', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock((('question', wagtail.wagtailcore.blocks.CharBlock()), ('answer', isi_mip.contrib.blocks.RichTextBlock())))))))), ('pdf', wagtail.wagtailcore.blocks.StructBlock((('file', wagtail.wagtaildocs.blocks.DocumentChooserBlock()), ('description', wagtail.wagtailcore.blocks.CharBlock())))))))))), ('columns_1_to_2', wagtail.wagtailcore.blocks.StructBlock((('left_column', wagtail.wagtailcore.blocks.StreamBlock((('heading', isi_mip.contrib.blocks.HeadingBlock()), ('rich_text', isi_mip.contrib.blocks.RichTextBlock()), ('horizontal_ruler', wagtail.wagtailcore.blocks.StreamBlock(())), ('embed', wagtail.wagtailembeds.blocks.EmbedBlock()), ('image', isi_mip.contrib.blocks.ImageBlock()), ('table', wagtail.contrib.table_block.blocks.TableBlock()), ('monospace_text', isi_mip.contrib.blocks.MonospaceTextBlock()), ('small_teaser', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock(required=True)), ('picture', wagtail.wagtailimages.blocks.ImageChooserBlock()), ('text', wagtail.wagtailcore.blocks.TextBlock(required=True)), ('link', wagtail.wagtailcore.blocks.PageChooserBlock(required=True))))), ('big_teaser', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock(required=True)), ('subtitle', wagtail.wagtailcore.blocks.CharBlock(required=False)), ('picture', wagtail.wagtailimages.blocks.ImageChooserBlock()), ('text', isi_mip.contrib.blocks.RichTextBlock()), ('external_link', wagtail.wagtailcore.blocks.URLBlock(help_text='Will be ignored if an internal link is provided', required=False)), ('internal_link', wagtail.wagtailcore.blocks.PageChooserBlock(help_text='If set, this has precedence over the external link.', required=False)), ('from_date', wagtail.wagtailcore.blocks.DateBlock(required=False)), ('to_date', wagtail.wagtailcore.blocks.DateBlock(required=False))))), ('isinumbers', wagtail.wagtailcore.blocks.StructBlock((('number1', wagtail.wagtailcore.blocks.StructBlock((('number', wagtail.wagtailcore.blocks.CharBlock()), ('title', wagtail.wagtailcore.blocks.CharBlock()), ('text', wagtail.wagtailcore.blocks.CharBlock())))), ('number2', wagtail.wagtailcore.blocks.StructBlock((('number', wagtail.wagtailcore.blocks.CharBlock()), ('title', wagtail.wagtailcore.blocks.CharBlock()), ('text', wagtail.wagtailcore.blocks.CharBlock()))))))), ('link', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock(required=True)), ('picture', wagtail.wagtailimages.blocks.ImageChooserBlock(required=False)), ('text', isi_mip.contrib.blocks.RichTextBlock(required=False)), ('link', wagtail.wagtailcore.blocks.URLBlock(required=False)), ('date', wagtail.wagtailcore.blocks.DateBlock(required=False))))), ('faqs', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock()), ('faqs', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock((('question', wagtail.wagtailcore.blocks.CharBlock()), ('answer', isi_mip.contrib.blocks.RichTextBlock())))))))), ('pdf', wagtail.wagtailcore.blocks.StructBlock((('file', wagtail.wagtaildocs.blocks.DocumentChooserBlock()), ('description', wagtail.wagtailcore.blocks.CharBlock()))))))), ('right_column', wagtail.wagtailcore.blocks.StreamBlock((('heading', isi_mip.contrib.blocks.HeadingBlock()), ('rich_text', isi_mip.contrib.blocks.RichTextBlock()), ('horizontal_ruler', wagtail.wagtailcore.blocks.StreamBlock(())), ('embed', wagtail.wagtailembeds.blocks.EmbedBlock()), ('image', isi_mip.contrib.blocks.ImageBlock()), ('table', wagtail.contrib.table_block.blocks.TableBlock()), ('monospace_text', isi_mip.contrib.blocks.MonospaceTextBlock()), ('small_teaser', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock(required=True)), ('picture', wagtail.wagtailimages.blocks.ImageChooserBlock()), ('text', wagtail.wagtailcore.blocks.TextBlock(required=True)), ('link', wagtail.wagtailcore.blocks.PageChooserBlock(required=True))))), ('big_teaser', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock(required=True)), ('subtitle', wagtail.wagtailcore.blocks.CharBlock(required=False)), ('picture', wagtail.wagtailimages.blocks.ImageChooserBlock()), ('text', isi_mip.contrib.blocks.RichTextBlock()), ('external_link', wagtail.wagtailcore.blocks.URLBlock(help_text='Will be ignored if an internal link is provided', required=False)), ('internal_link', wagtail.wagtailcore.blocks.PageChooserBlock(help_text='If set, this has precedence over the external link.', required=False)), ('from_date', wagtail.wagtailcore.blocks.DateBlock(required=False)), ('to_date', wagtail.wagtailcore.blocks.DateBlock(required=False))))), ('isinumbers', wagtail.wagtailcore.blocks.StructBlock((('number1', wagtail.wagtailcore.blocks.StructBlock((('number', wagtail.wagtailcore.blocks.CharBlock()), ('title', wagtail.wagtailcore.blocks.CharBlock()), ('text', wagtail.wagtailcore.blocks.CharBlock())))), ('number2', wagtail.wagtailcore.blocks.StructBlock((('number', wagtail.wagtailcore.blocks.CharBlock()), ('title', wagtail.wagtailcore.blocks.CharBlock()), ('text', wagtail.wagtailcore.blocks.CharBlock()))))))), ('link', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock(required=True)), ('picture', wagtail.wagtailimages.blocks.ImageChooserBlock(required=False)), ('text', isi_mip.contrib.blocks.RichTextBlock(required=False)), ('link', wagtail.wagtailcore.blocks.URLBlock(required=False)), ('date', wagtail.wagtailcore.blocks.DateBlock(required=False))))), ('faqs', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock()), ('faqs', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock((('question', wagtail.wagtailcore.blocks.CharBlock()), ('answer', isi_mip.contrib.blocks.RichTextBlock())))))))), ('pdf', wagtail.wagtailcore.blocks.StructBlock((('file', wagtail.wagtaildocs.blocks.DocumentChooserBlock()), ('description', wagtail.wagtailcore.blocks.CharBlock())))))))))), ('columns_2_to_1', wagtail.wagtailcore.blocks.StructBlock((('left_column', wagtail.wagtailcore.blocks.StreamBlock((('heading', isi_mip.contrib.blocks.HeadingBlock()), ('rich_text', isi_mip.contrib.blocks.RichTextBlock()), ('horizontal_ruler', wagtail.wagtailcore.blocks.StreamBlock(())), ('embed', wagtail.wagtailembeds.blocks.EmbedBlock()), ('image', isi_mip.contrib.blocks.ImageBlock()), ('table', wagtail.contrib.table_block.blocks.TableBlock()), ('monospace_text', isi_mip.contrib.blocks.MonospaceTextBlock()), ('small_teaser', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock(required=True)), ('picture', wagtail.wagtailimages.blocks.ImageChooserBlock()), ('text', wagtail.wagtailcore.blocks.TextBlock(required=True)), ('link', wagtail.wagtailcore.blocks.PageChooserBlock(required=True))))), ('big_teaser', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock(required=True)), ('subtitle', wagtail.wagtailcore.blocks.CharBlock(required=False)), ('picture', wagtail.wagtailimages.blocks.ImageChooserBlock()), ('text', isi_mip.contrib.blocks.RichTextBlock()), ('external_link', wagtail.wagtailcore.blocks.URLBlock(help_text='Will be ignored if an internal link is provided', required=False)), ('internal_link', wagtail.wagtailcore.blocks.PageChooserBlock(help_text='If set, this has precedence over the external link.', required=False)), ('from_date', wagtail.wagtailcore.blocks.DateBlock(required=False)), ('to_date', wagtail.wagtailcore.blocks.DateBlock(required=False))))), ('isinumbers', wagtail.wagtailcore.blocks.StructBlock((('number1', wagtail.wagtailcore.blocks.StructBlock((('number', wagtail.wagtailcore.blocks.CharBlock()), ('title', wagtail.wagtailcore.blocks.CharBlock()), ('text', wagtail.wagtailcore.blocks.CharBlock())))), ('number2', wagtail.wagtailcore.blocks.StructBlock((('number', wagtail.wagtailcore.blocks.CharBlock()), ('title', wagtail.wagtailcore.blocks.CharBlock()), ('text', wagtail.wagtailcore.blocks.CharBlock()))))))), ('link', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock(required=True)), ('picture', wagtail.wagtailimages.blocks.ImageChooserBlock(required=False)), ('text', isi_mip.contrib.blocks.RichTextBlock(required=False)), ('link', wagtail.wagtailcore.blocks.URLBlock(required=False)), ('date', wagtail.wagtailcore.blocks.DateBlock(required=False))))), ('faqs', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock()), ('faqs', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock((('question', wagtail.wagtailcore.blocks.CharBlock()), ('answer', isi_mip.contrib.blocks.RichTextBlock())))))))), ('pdf', wagtail.wagtailcore.blocks.StructBlock((('file', wagtail.wagtaildocs.blocks.DocumentChooserBlock()), ('description', wagtail.wagtailcore.blocks.CharBlock()))))))), ('right_column', wagtail.wagtailcore.blocks.StreamBlock((('heading', isi_mip.contrib.blocks.HeadingBlock()), ('rich_text', isi_mip.contrib.blocks.RichTextBlock()), ('horizontal_ruler', wagtail.wagtailcore.blocks.StreamBlock(())), ('embed', wagtail.wagtailembeds.blocks.EmbedBlock()), ('image', isi_mip.contrib.blocks.ImageBlock()), ('table', wagtail.contrib.table_block.blocks.TableBlock()), ('monospace_text', isi_mip.contrib.blocks.MonospaceTextBlock()), ('small_teaser', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock(required=True)), ('picture', wagtail.wagtailimages.blocks.ImageChooserBlock()), ('text', wagtail.wagtailcore.blocks.TextBlock(required=True)), ('link', wagtail.wagtailcore.blocks.PageChooserBlock(required=True))))), ('big_teaser', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock(required=True)), ('subtitle', wagtail.wagtailcore.blocks.CharBlock(required=False)), ('picture', wagtail.wagtailimages.blocks.ImageChooserBlock()), ('text', isi_mip.contrib.blocks.RichTextBlock()), ('external_link', wagtail.wagtailcore.blocks.URLBlock(help_text='Will be ignored if an internal link is provided', required=False)), ('internal_link', wagtail.wagtailcore.blocks.PageChooserBlock(help_text='If set, this has precedence over the external link.', required=False)), ('from_date', wagtail.wagtailcore.blocks.DateBlock(required=False)), ('to_date', wagtail.wagtailcore.blocks.DateBlock(required=False))))), ('isinumbers', wagtail.wagtailcore.blocks.StructBlock((('number1', wagtail.wagtailcore.blocks.StructBlock((('number', wagtail.wagtailcore.blocks.CharBlock()), ('title', wagtail.wagtailcore.blocks.CharBlock()), ('text', wagtail.wagtailcore.blocks.CharBlock())))), ('number2', wagtail.wagtailcore.blocks.StructBlock((('number', wagtail.wagtailcore.blocks.CharBlock()), ('title', wagtail.wagtailcore.blocks.CharBlock()), ('text', wagtail.wagtailcore.blocks.CharBlock()))))))), ('link', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock(required=True)), ('picture', wagtail.wagtailimages.blocks.ImageChooserBlock(required=False)), ('text', isi_mip.contrib.blocks.RichTextBlock(required=False)), ('link', wagtail.wagtailcore.blocks.URLBlock(required=False)), ('date', wagtail.wagtailcore.blocks.DateBlock(required=False))))), ('faqs', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock()), ('faqs', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock((('question', wagtail.wagtailcore.blocks.CharBlock()), ('answer', isi_mip.contrib.blocks.RichTextBlock())))))))), ('pdf', wagtail.wagtailcore.blocks.StructBlock((('file', wagtail.wagtaildocs.blocks.DocumentChooserBlock()), ('description', wagtail.wagtailcore.blocks.CharBlock())))))))))), ('columns_1_to_1_to_1', wagtail.wagtailcore.blocks.StructBlock((('left_column', wagtail.wagtailcore.blocks.StreamBlock((('heading', isi_mip.contrib.blocks.HeadingBlock()), ('rich_text', isi_mip.contrib.blocks.RichTextBlock()), ('horizontal_ruler', wagtail.wagtailcore.blocks.StreamBlock(())), ('embed', wagtail.wagtailembeds.blocks.EmbedBlock()), ('image', isi_mip.contrib.blocks.ImageBlock()), ('table', wagtail.contrib.table_block.blocks.TableBlock()), ('monospace_text', isi_mip.contrib.blocks.MonospaceTextBlock()), ('small_teaser', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock(required=True)), ('picture', wagtail.wagtailimages.blocks.ImageChooserBlock()), ('text', wagtail.wagtailcore.blocks.TextBlock(required=True)), ('link', wagtail.wagtailcore.blocks.PageChooserBlock(required=True))))), ('big_teaser', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock(required=True)), ('subtitle', wagtail.wagtailcore.blocks.CharBlock(required=False)), ('picture', wagtail.wagtailimages.blocks.ImageChooserBlock()), ('text', isi_mip.contrib.blocks.RichTextBlock()), ('external_link', wagtail.wagtailcore.blocks.URLBlock(help_text='Will be ignored if an internal link is provided', required=False)), ('internal_link', wagtail.wagtailcore.blocks.PageChooserBlock(help_text='If set, this has precedence over the external link.', required=False)), ('from_date', wagtail.wagtailcore.blocks.DateBlock(required=False)), ('to_date', wagtail.wagtailcore.blocks.DateBlock(required=False))))), ('isinumbers', wagtail.wagtailcore.blocks.StructBlock((('number1', wagtail.wagtailcore.blocks.StructBlock((('number', wagtail.wagtailcore.blocks.CharBlock()), ('title', wagtail.wagtailcore.blocks.CharBlock()), ('text', wagtail.wagtailcore.blocks.CharBlock())))), ('number2', wagtail.wagtailcore.blocks.StructBlock((('number', wagtail.wagtailcore.blocks.CharBlock()), ('title', wagtail.wagtailcore.blocks.CharBlock()), ('text', wagtail.wagtailcore.blocks.CharBlock()))))))), ('link', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock(required=True)), ('picture', wagtail.wagtailimages.blocks.ImageChooserBlock(required=False)), ('text', isi_mip.contrib.blocks.RichTextBlock(required=False)), ('link', wagtail.wagtailcore.blocks.URLBlock(required=False)), ('date', wagtail.wagtailcore.blocks.DateBlock(required=False))))), ('faqs', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock()), ('faqs', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock((('question', wagtail.wagtailcore.blocks.CharBlock()), ('answer', isi_mip.contrib.blocks.RichTextBlock())))))))), ('pdf', wagtail.wagtailcore.blocks.StructBlock((('file', wagtail.wagtaildocs.blocks.DocumentChooserBlock()), ('description', wagtail.wagtailcore.blocks.CharBlock()))))))), ('right_column', wagtail.wagtailcore.blocks.StreamBlock((('heading', isi_mip.contrib.blocks.HeadingBlock()), ('rich_text', isi_mip.contrib.blocks.RichTextBlock()), ('horizontal_ruler', wagtail.wagtailcore.blocks.StreamBlock(())), ('embed', wagtail.wagtailembeds.blocks.EmbedBlock()), ('image', isi_mip.contrib.blocks.ImageBlock()), ('table', wagtail.contrib.table_block.blocks.TableBlock()), ('monospace_text', isi_mip.contrib.blocks.MonospaceTextBlock()), ('small_teaser', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock(required=True)), ('picture', wagtail.wagtailimages.blocks.ImageChooserBlock()), ('text', wagtail.wagtailcore.blocks.TextBlock(required=True)), ('link', wagtail.wagtailcore.blocks.PageChooserBlock(required=True))))), ('big_teaser', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock(required=True)), ('subtitle', wagtail.wagtailcore.blocks.CharBlock(required=False)), ('picture', wagtail.wagtailimages.blocks.ImageChooserBlock()), ('text', isi_mip.contrib.blocks.RichTextBlock()), ('external_link', wagtail.wagtailcore.blocks.URLBlock(help_text='Will be ignored if an internal link is provided', required=False)), ('internal_link', wagtail.wagtailcore.blocks.PageChooserBlock(help_text='If set, this has precedence over the external link.', required=False)), ('from_date', wagtail.wagtailcore.blocks.DateBlock(required=False)), ('to_date', wagtail.wagtailcore.blocks.DateBlock(required=False))))), ('isinumbers', wagtail.wagtailcore.blocks.StructBlock((('number1', wagtail.wagtailcore.blocks.StructBlock((('number', wagtail.wagtailcore.blocks.CharBlock()), ('title', wagtail.wagtailcore.blocks.CharBlock()), ('text', wagtail.wagtailcore.blocks.CharBlock())))), ('number2', wagtail.wagtailcore.blocks.StructBlock((('number', wagtail.wagtailcore.blocks.CharBlock()), ('title', wagtail.wagtailcore.blocks.CharBlock()), ('text', wagtail.wagtailcore.blocks.CharBlock()))))))), ('link', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock(required=True)), ('picture', wagtail.wagtailimages.blocks.ImageChooserBlock(required=False)), ('text', isi_mip.contrib.blocks.RichTextBlock(required=False)), ('link', wagtail.wagtailcore.blocks.URLBlock(required=False)), ('date', wagtail.wagtailcore.blocks.DateBlock(required=False))))), ('faqs', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock()), ('faqs', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock((('question', wagtail.wagtailcore.blocks.CharBlock()), ('answer', isi_mip.contrib.blocks.RichTextBlock())))))))), ('pdf', wagtail.wagtailcore.blocks.StructBlock((('file', wagtail.wagtaildocs.blocks.DocumentChooserBlock()), ('description', wagtail.wagtailcore.blocks.CharBlock()))))))), ('center_column', wagtail.wagtailcore.blocks.StreamBlock((('heading', isi_mip.contrib.blocks.HeadingBlock()), ('rich_text', isi_mip.contrib.blocks.RichTextBlock()), ('horizontal_ruler', wagtail.wagtailcore.blocks.StreamBlock(())), ('embed', wagtail.wagtailembeds.blocks.EmbedBlock()), ('image', isi_mip.contrib.blocks.ImageBlock()), ('table', wagtail.contrib.table_block.blocks.TableBlock()), ('monospace_text', isi_mip.contrib.blocks.MonospaceTextBlock()), ('small_teaser', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock(required=True)), ('picture', wagtail.wagtailimages.blocks.ImageChooserBlock()), ('text', wagtail.wagtailcore.blocks.TextBlock(required=True)), ('link', wagtail.wagtailcore.blocks.PageChooserBlock(required=True))))), ('big_teaser', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock(required=True)), ('subtitle', wagtail.wagtailcore.blocks.CharBlock(required=False)), ('picture', wagtail.wagtailimages.blocks.ImageChooserBlock()), ('text', isi_mip.contrib.blocks.RichTextBlock()), ('external_link', wagtail.wagtailcore.blocks.URLBlock(help_text='Will be ignored if an internal link is provided', required=False)), ('internal_link', wagtail.wagtailcore.blocks.PageChooserBlock(help_text='If set, this has precedence over the external link.', required=False)), ('from_date', wagtail.wagtailcore.blocks.DateBlock(required=False)), ('to_date', wagtail.wagtailcore.blocks.DateBlock(required=False))))), ('isinumbers', wagtail.wagtailcore.blocks.StructBlock((('number1', wagtail.wagtailcore.blocks.StructBlock((('number', wagtail.wagtailcore.blocks.CharBlock()), ('title', wagtail.wagtailcore.blocks.CharBlock()), ('text', wagtail.wagtailcore.blocks.CharBlock())))), ('number2', wagtail.wagtailcore.blocks.StructBlock((('number', wagtail.wagtailcore.blocks.CharBlock()), ('title', wagtail.wagtailcore.blocks.CharBlock()), ('text', wagtail.wagtailcore.blocks.CharBlock()))))))), ('link', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock(required=True)), ('picture', wagtail.wagtailimages.blocks.ImageChooserBlock(required=False)), ('text', isi_mip.contrib.blocks.RichTextBlock(required=False)), ('link', wagtail.wagtailcore.blocks.URLBlock(required=False)), ('date', wagtail.wagtailcore.blocks.DateBlock(required=False))))), ('faqs', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock()), ('faqs', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock((('question', wagtail.wagtailcore.blocks.CharBlock()), ('answer', isi_mip.contrib.blocks.RichTextBlock())))))))), ('pdf', wagtail.wagtailcore.blocks.StructBlock((('file', wagtail.wagtaildocs.blocks.DocumentChooserBlock()), ('description', wagtail.wagtailcore.blocks.CharBlock())))))))))), ('columns_1_to_1_to_1_to_1', wagtail.wagtailcore.blocks.StructBlock((('first_column', wagtail.wagtailcore.blocks.StreamBlock((('heading', isi_mip.contrib.blocks.HeadingBlock()), ('rich_text', isi_mip.contrib.blocks.RichTextBlock()), ('horizontal_ruler', wagtail.wagtailcore.blocks.StreamBlock(())), ('embed', wagtail.wagtailembeds.blocks.EmbedBlock()), ('image', isi_mip.contrib.blocks.ImageBlock()), ('table', wagtail.contrib.table_block.blocks.TableBlock()), ('monospace_text', isi_mip.contrib.blocks.MonospaceTextBlock()), ('small_teaser', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock(required=True)), ('picture', wagtail.wagtailimages.blocks.ImageChooserBlock()), ('text', wagtail.wagtailcore.blocks.TextBlock(required=True)), ('link', wagtail.wagtailcore.blocks.PageChooserBlock(required=True))))), ('big_teaser', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock(required=True)), ('subtitle', wagtail.wagtailcore.blocks.CharBlock(required=False)), ('picture', wagtail.wagtailimages.blocks.ImageChooserBlock()), ('text', isi_mip.contrib.blocks.RichTextBlock()), ('external_link', wagtail.wagtailcore.blocks.URLBlock(help_text='Will be ignored if an internal link is provided', required=False)), ('internal_link', wagtail.wagtailcore.blocks.PageChooserBlock(help_text='If set, this has precedence over the external link.', required=False)), ('from_date', wagtail.wagtailcore.blocks.DateBlock(required=False)), ('to_date', wagtail.wagtailcore.blocks.DateBlock(required=False))))), ('isinumbers', wagtail.wagtailcore.blocks.StructBlock((('number1', wagtail.wagtailcore.blocks.StructBlock((('number', wagtail.wagtailcore.blocks.CharBlock()), ('title', wagtail.wagtailcore.blocks.CharBlock()), ('text', wagtail.wagtailcore.blocks.CharBlock())))), ('number2', wagtail.wagtailcore.blocks.StructBlock((('number', wagtail.wagtailcore.blocks.CharBlock()), ('title', wagtail.wagtailcore.blocks.CharBlock()), ('text', wagtail.wagtailcore.blocks.CharBlock()))))))), ('link', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock(required=True)), ('picture', wagtail.wagtailimages.blocks.ImageChooserBlock(required=False)), ('text', isi_mip.contrib.blocks.RichTextBlock(required=False)), ('link', wagtail.wagtailcore.blocks.URLBlock(required=False)), ('date', wagtail.wagtailcore.blocks.DateBlock(required=False))))), ('faqs', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock()), ('faqs', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock((('question', wagtail.wagtailcore.blocks.CharBlock()), ('answer', isi_mip.contrib.blocks.RichTextBlock())))))))), ('pdf', wagtail.wagtailcore.blocks.StructBlock((('file', wagtail.wagtaildocs.blocks.DocumentChooserBlock()), ('description', wagtail.wagtailcore.blocks.CharBlock()))))))), ('second_column', wagtail.wagtailcore.blocks.StreamBlock((('heading', isi_mip.contrib.blocks.HeadingBlock()), ('rich_text', isi_mip.contrib.blocks.RichTextBlock()), ('horizontal_ruler', wagtail.wagtailcore.blocks.StreamBlock(())), ('embed', wagtail.wagtailembeds.blocks.EmbedBlock()), ('image', isi_mip.contrib.blocks.ImageBlock()), ('table', wagtail.contrib.table_block.blocks.TableBlock()), ('monospace_text', isi_mip.contrib.blocks.MonospaceTextBlock()), ('small_teaser', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock(required=True)), ('picture', wagtail.wagtailimages.blocks.ImageChooserBlock()), ('text', wagtail.wagtailcore.blocks.TextBlock(required=True)), ('link', wagtail.wagtailcore.blocks.PageChooserBlock(required=True))))), ('big_teaser', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock(required=True)), ('subtitle', wagtail.wagtailcore.blocks.CharBlock(required=False)), ('picture', wagtail.wagtailimages.blocks.ImageChooserBlock()), ('text', isi_mip.contrib.blocks.RichTextBlock()), ('external_link', wagtail.wagtailcore.blocks.URLBlock(help_text='Will be ignored if an internal link is provided', required=False)), ('internal_link', wagtail.wagtailcore.blocks.PageChooserBlock(help_text='If set, this has precedence over the external link.', required=False)), ('from_date', wagtail.wagtailcore.blocks.DateBlock(required=False)), ('to_date', wagtail.wagtailcore.blocks.DateBlock(required=False))))), ('isinumbers', wagtail.wagtailcore.blocks.StructBlock((('number1', wagtail.wagtailcore.blocks.StructBlock((('number', wagtail.wagtailcore.blocks.CharBlock()), ('title', wagtail.wagtailcore.blocks.CharBlock()), ('text', wagtail.wagtailcore.blocks.CharBlock())))), ('number2', wagtail.wagtailcore.blocks.StructBlock((('number', wagtail.wagtailcore.blocks.CharBlock()), ('title', wagtail.wagtailcore.blocks.CharBlock()), ('text', wagtail.wagtailcore.blocks.CharBlock()))))))), ('link', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock(required=True)), ('picture', wagtail.wagtailimages.blocks.ImageChooserBlock(required=False)), ('text', isi_mip.contrib.blocks.RichTextBlock(required=False)), ('link', wagtail.wagtailcore.blocks.URLBlock(required=False)), ('date', wagtail.wagtailcore.blocks.DateBlock(required=False))))), ('faqs', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock()), ('faqs', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock((('question', wagtail.wagtailcore.blocks.CharBlock()), ('answer', isi_mip.contrib.blocks.RichTextBlock())))))))), ('pdf', wagtail.wagtailcore.blocks.StructBlock((('file', wagtail.wagtaildocs.blocks.DocumentChooserBlock()), ('description', wagtail.wagtailcore.blocks.CharBlock()))))))), ('third_column', wagtail.wagtailcore.blocks.StreamBlock((('heading', isi_mip.contrib.blocks.HeadingBlock()), ('rich_text', isi_mip.contrib.blocks.RichTextBlock()), ('horizontal_ruler', wagtail.wagtailcore.blocks.StreamBlock(())), ('embed', wagtail.wagtailembeds.blocks.EmbedBlock()), ('image', isi_mip.contrib.blocks.ImageBlock()), ('table', wagtail.contrib.table_block.blocks.TableBlock()), ('monospace_text', isi_mip.contrib.blocks.MonospaceTextBlock()), ('small_teaser', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock(required=True)), ('picture', wagtail.wagtailimages.blocks.ImageChooserBlock()), ('text', wagtail.wagtailcore.blocks.TextBlock(required=True)), ('link', wagtail.wagtailcore.blocks.PageChooserBlock(required=True))))), ('big_teaser', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock(required=True)), ('subtitle', wagtail.wagtailcore.blocks.CharBlock(required=False)), ('picture', wagtail.wagtailimages.blocks.ImageChooserBlock()), ('text', isi_mip.contrib.blocks.RichTextBlock()), ('external_link', wagtail.wagtailcore.blocks.URLBlock(help_text='Will be ignored if an internal link is provided', required=False)), ('internal_link', wagtail.wagtailcore.blocks.PageChooserBlock(help_text='If set, this has precedence over the external link.', required=False)), ('from_date', wagtail.wagtailcore.blocks.DateBlock(required=False)), ('to_date', wagtail.wagtailcore.blocks.DateBlock(required=False))))), ('isinumbers', wagtail.wagtailcore.blocks.StructBlock((('number1', wagtail.wagtailcore.blocks.StructBlock((('number', wagtail.wagtailcore.blocks.CharBlock()), ('title', wagtail.wagtailcore.blocks.CharBlock()), ('text', wagtail.wagtailcore.blocks.CharBlock())))), ('number2', wagtail.wagtailcore.blocks.StructBlock((('number', wagtail.wagtailcore.blocks.CharBlock()), ('title', wagtail.wagtailcore.blocks.CharBlock()), ('text', wagtail.wagtailcore.blocks.CharBlock()))))))), ('link', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock(required=True)), ('picture', wagtail.wagtailimages.blocks.ImageChooserBlock(required=False)), ('text', isi_mip.contrib.blocks.RichTextBlock(required=False)), ('link', wagtail.wagtailcore.blocks.URLBlock(required=False)), ('date', wagtail.wagtailcore.blocks.DateBlock(required=False))))), ('faqs', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock()), ('faqs', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock((('question', wagtail.wagtailcore.blocks.CharBlock()), ('answer', isi_mip.contrib.blocks.RichTextBlock())))))))), ('pdf', wagtail.wagtailcore.blocks.StructBlock((('file', wagtail.wagtaildocs.blocks.DocumentChooserBlock()), ('description', wagtail.wagtailcore.blocks.CharBlock()))))))), ('fourth_column', wagtail.wagtailcore.blocks.StreamBlock((('heading', isi_mip.contrib.blocks.HeadingBlock()), ('rich_text', isi_mip.contrib.blocks.RichTextBlock()), ('horizontal_ruler', wagtail.wagtailcore.blocks.StreamBlock(())), ('embed', wagtail.wagtailembeds.blocks.EmbedBlock()), ('image', isi_mip.contrib.blocks.ImageBlock()), ('table', wagtail.contrib.table_block.blocks.TableBlock()), ('monospace_text', isi_mip.contrib.blocks.MonospaceTextBlock()), ('small_teaser', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock(required=True)), ('picture', wagtail.wagtailimages.blocks.ImageChooserBlock()), ('text', wagtail.wagtailcore.blocks.TextBlock(required=True)), ('link', wagtail.wagtailcore.blocks.PageChooserBlock(required=True))))), ('big_teaser', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock(required=True)), ('subtitle', wagtail.wagtailcore.blocks.CharBlock(required=False)), ('picture', wagtail.wagtailimages.blocks.ImageChooserBlock()), ('text', isi_mip.contrib.blocks.RichTextBlock()), ('external_link', wagtail.wagtailcore.blocks.URLBlock(help_text='Will be ignored if an internal link is provided', required=False)), ('internal_link', wagtail.wagtailcore.blocks.PageChooserBlock(help_text='If set, this has precedence over the external link.', required=False)), ('from_date', wagtail.wagtailcore.blocks.DateBlock(required=False)), ('to_date', wagtail.wagtailcore.blocks.DateBlock(required=False))))), ('isinumbers', wagtail.wagtailcore.blocks.StructBlock((('number1', wagtail.wagtailcore.blocks.StructBlock((('number', wagtail.wagtailcore.blocks.CharBlock()), ('title', wagtail.wagtailcore.blocks.CharBlock()), ('text', wagtail.wagtailcore.blocks.CharBlock())))), ('number2', wagtail.wagtailcore.blocks.StructBlock((('number', wagtail.wagtailcore.blocks.CharBlock()), ('title', wagtail.wagtailcore.blocks.CharBlock()), ('text', wagtail.wagtailcore.blocks.CharBlock()))))))), ('link', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock(required=True)), ('picture', wagtail.wagtailimages.blocks.ImageChooserBlock(required=False)), ('text', isi_mip.contrib.blocks.RichTextBlock(required=False)), ('link', wagtail.wagtailcore.blocks.URLBlock(required=False)), ('date', wagtail.wagtailcore.blocks.DateBlock(required=False))))), ('faqs', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock()), ('faqs', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock((('question', wagtail.wagtailcore.blocks.CharBlock()), ('answer', isi_mip.contrib.blocks.RichTextBlock())))))))), ('pdf', wagtail.wagtailcore.blocks.StructBlock((('file', wagtail.wagtaildocs.blocks.DocumentChooserBlock()), ('description', wagtail.wagtailcore.blocks.CharBlock())))))))))), ('pdf', wagtail.wagtailcore.blocks.StructBlock((('file', wagtail.wagtaildocs.blocks.DocumentChooserBlock()), ('description', wagtail.wagtailcore.blocks.CharBlock())))), ('paper', wagtail.wagtailcore.blocks.StructBlock((('picture', wagtail.wagtailimages.blocks.ImageChooserBlock(required=False)), ('author', wagtail.wagtailcore.blocks.CharBlock()), ('title', wagtail.wagtailcore.blocks.CharBlock()), ('journal', wagtail.wagtailcore.blocks.CharBlock()), ('link', wagtail.wagtailcore.blocks.URLBlock())), template='widgets/page-teaser-wide.html')), ('bigteaser', wagtail.wagtailcore.blocks.StructBlock((('title', wagtail.wagtailcore.blocks.CharBlock(required=True)), ('subtitle', wagtail.wagtailcore.blocks.CharBlock(required=False)), ('picture', wagtail.wagtailimages.blocks.ImageChooserBlock()), ('text', isi_mip.contrib.blocks.RichTextBlock()), ('external_link', wagtail.wagtailcore.blocks.URLBlock(help_text='Will be ignored if an internal link is provided', required=False)), ('internal_link', wagtail.wagtailcore.blocks.PageChooserBlock(help_text='If set, this has precedence over the external link.', required=False)), ('from_date', wagtail.wagtailcore.blocks.DateBlock(required=False)), ('to_date', wagtail.wagtailcore.blocks.DateBlock(required=False))))), ('contact', wagtail.wagtailcore.blocks.StructBlock((('sectors', wagtail.wagtailcore.blocks.ListBlock(isi_mip.pages.blocks.SectorBlock)),))))),
        ),
    ]
