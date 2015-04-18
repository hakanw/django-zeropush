# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from south.modelsinspector import get_model_meta
from django.db import models
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
import django

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')

# Django 1.5+ compatibility
if django.VERSION >= (1, 5):
    try:
        from django.contrib.auth import get_user_model
        User = get_user_model()
        username_field = User.USERNAME_FIELD
    except ImproperlyConfigured:
        # The the users model might not be read yet.
        # This can happen is when setting up the create_api_key signal, in your
        # custom user module.
        User = None
        username_field = None
else:
    from django.contrib.auth.models import User
    username_field = 'username'

AUTH_USER_META = get_model_meta(User)
AUTH_USER_META.update({'object_name': AUTH_USER_MODEL.split('.')[-1]})


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'DelayedPushNotification.to_device'
        db.add_column(u'zeropush_delayedpushnotification', 'to_device',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['zeropush.PushDevice'], null=True, blank=True),
                      keep_default=False)


        # Changing field 'DelayedPushNotification.to_user'
        db.alter_column(u'zeropush_delayedpushnotification', 'to_user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm[AUTH_USER_MODEL], null=True))

    def backwards(self, orm):
        # Deleting field 'DelayedPushNotification.to_device'
        db.delete_column(u'zeropush_delayedpushnotification', 'to_device_id')


        # User chose to not deal with backwards NULL issues for 'DelayedPushNotification.to_user'
        raise RuntimeError("Cannot reverse this migration. 'DelayedPushNotification.to_user' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'DelayedPushNotification.to_user'
        db.alter_column(u'zeropush_delayedpushnotification', 'to_user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm[AUTH_USER_MODEL]))

    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        AUTH_USER_MODEL: {
            'Meta': AUTH_USER_META,
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'zeropush.delayedpushnotification': {
            'Meta': {'object_name': 'DelayedPushNotification'},
            'alert': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'error': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'expired': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info_json': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'num_tries': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'sent': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'sound': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'to_device': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['zeropush.PushDevice']", 'null': 'True', 'blank': 'True'}),
            'to_user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['%s']" % AUTH_USER_MODEL, 'null': 'True', 'blank': 'True'})
        },
        u'zeropush.pushdevice': {
            'Meta': {'unique_together': "(('user', 'token'),)", 'object_name': 'PushDevice'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'token': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['%s']" % AUTH_USER_MODEL, 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['zeropush']