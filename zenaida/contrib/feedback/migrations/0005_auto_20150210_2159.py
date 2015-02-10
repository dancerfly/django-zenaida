# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def forward(apps, schema_editor):
    TalkbackFeedbackItem = apps.get_model("talkback", "FeedbackItem")
    ZenaidaFeedbackItem = apps.get_model("talkback", "FeedbackItem")
    # Delete the table created by `talkback`. Presumably
    # this will be empty since it was just created in talkback 0001_initial.
    schema_editor.delete_model(TalkbackFeedbackItem)
    # Move the zenaida table into it's place:
    schema_editor.alter_db_table(ZenaidaFeedbackItem, "feedback_feedbackitem", "talkback_feedbackitem")
    # Create an empty table for zenaida feedback in place:
    schema_editor.delete_model(ZenaidaFeedbackItem)


def backward(apps, schema_editor):
    TalkbackFeedbackItem = apps.get_model("talkback", "FeedbackItem")
    ZenaidaFeedbackItem = apps.get_model("talkback", "FeedbackItem")
    schema_editor.alter_db_table(ZenaidaFeedbackItem, "talkback_feedbackitem", "feedback_feedbackitem")
    schema_editor.create_model(ZenaidaFeedbackItem)


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0004_auto_20140622_1737'),
        ('talkback', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(forward, backward),
    ]
