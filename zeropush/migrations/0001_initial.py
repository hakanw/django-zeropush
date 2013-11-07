# -*- coding: utf-8 -*-
import datetime
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
        # Adding model 'PushDevice'
        db.create_table(u'zeropush_pushdevice', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm[AUTH_USER_MODEL])),
            ('token', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
        ))
        db.send_create_signal(u'zeropush', ['PushDevice'])

        # Adding unique constraint on 'PushDevice', fields ['user', 'token']
        db.create_unique(u'zeropush_pushdevice', ['user_id', 'token'])

        # Adding model 'DelayedPushNotification'
        db.create_table(u'zeropush_delayedpushnotification', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('to_user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm[AUTH_USER_MODEL])),
            ('alert', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('sound', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('info', self.gf('django.db.models.fields.CharField')(max_length=512, null=True, blank=True)),
            ('sent', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
            ('num_tries', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('error', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('expired', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'zeropush', ['DelayedPushNotification'])


    def backwards(self, orm):
        # Removing unique constraint on 'PushDevice', fields ['user', 'token']
        db.delete_unique(u'zeropush_pushdevice', ['user_id', 'token'])

        # Deleting model 'PushDevice'
        db.delete_table(u'zeropush_pushdevice')

        # Deleting model 'DelayedPushNotification'
        db.delete_table(u'zeropush_delayedpushnotification')


    models = {
        AUTH_USER_MODEL: {
                    'Meta': AUTH_USER_META,
                    'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
                    'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
                    'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
                    'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
                    'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
                    'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
                    'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
                    'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
                    'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
                    'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
                    'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
                    'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
                    'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
                },
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
        u'zeropush.delayedpushnotification': {
            'Meta': {'object_name': 'DelayedPushNotification'},
            'alert': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'error': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'expired': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'num_tries': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'sent': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'sound': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'to_user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['%s']" % AUTH_USER_MODEL})
        },
        u'zeropush.pushdevice': {
            'Meta': {'unique_together': "(('user', 'token'),)", 'object_name': 'PushDevice'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'token': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['%s']" % AUTH_USER_MODEL})
        }
    }

    complete_apps = ['zeropush']