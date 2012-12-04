# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Activity'
        db.create_table('workflow_activity', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('kind', self.gf('django.db.models.fields.CharField')(default='standard', max_length=10)),
            ('process', self.gf('django.db.models.fields.related.ForeignKey')(related_name='activities', to=orm['workflow.Process'])),
            ('push_application', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='push_activities', null=True, to=orm['workflow.PushApplication'])),
            ('pushapp_param', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('application', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='activities', null=True, to=orm['workflow.Application'])),
            ('app_param', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('subflow', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='parent_activities', null=True, to=orm['workflow.Process'])),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('autostart', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('autofinish', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('join_mode', self.gf('django.db.models.fields.CharField')(default='xor', max_length=3)),
            ('split_mode', self.gf('django.db.models.fields.CharField')(default='and', max_length=3)),
        ))
        db.send_create_signal('workflow', ['Activity'])

        # Adding unique constraint on 'Activity', fields ['title', 'process']
        db.create_unique('workflow_activity', ['title', 'process_id'])

        # Adding M2M table for field roles on 'Activity'
        db.create_table('workflow_activity_roles', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('activity', models.ForeignKey(orm['workflow.activity'], null=False)),
            ('group', models.ForeignKey(orm['auth.group'], null=False))
        ))
        db.create_unique('workflow_activity_roles', ['activity_id', 'group_id'])

        # Adding model 'Process'
        db.create_table('workflow_process', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('enabled', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('begin', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='bprocess', null=True, to=orm['workflow.Activity'])),
            ('end', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='eprocess', null=True, to=orm['workflow.Activity'])),
            ('priority', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('workflow', ['Process'])

        # Adding model 'Application'
        db.create_table('workflow_application', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('suffix', self.gf('django.db.models.fields.CharField')(default='w', max_length=1, null=True, blank=True)),
        ))
        db.send_create_signal('workflow', ['Application'])

        # Adding model 'PushApplication'
        db.create_table('workflow_pushapplication', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal('workflow', ['PushApplication'])

        # Adding model 'Transition'
        db.create_table('workflow_transition', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('process', self.gf('django.db.models.fields.related.ForeignKey')(related_name='transitions', to=orm['workflow.Process'])),
            ('input', self.gf('django.db.models.fields.related.ForeignKey')(related_name='transition_inputs', to=orm['workflow.Activity'])),
            ('condition', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('output', self.gf('django.db.models.fields.related.ForeignKey')(related_name='transition_outputs', to=orm['workflow.Activity'])),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('precondition', self.gf('django.db.models.fields.SlugField')(max_length=50, null=True, blank=True)),
        ))
        db.send_create_signal('workflow', ['Transition'])

        # Adding model 'UserProfile'
        db.create_table('workflow_userprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], unique=True)),
            ('web_host', self.gf('django.db.models.fields.CharField')(default='localhost:8000', max_length=100)),
            ('notified', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('last_notif', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 12, 4, 0, 0))),
            ('nb_wi_notif', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('notif_delay', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('urgent_priority', self.gf('django.db.models.fields.IntegerField')(default=5)),
        ))
        db.send_create_signal('workflow', ['UserProfile'])


    def backwards(self, orm):
        # Removing unique constraint on 'Activity', fields ['title', 'process']
        db.delete_unique('workflow_activity', ['title', 'process_id'])

        # Deleting model 'Activity'
        db.delete_table('workflow_activity')

        # Removing M2M table for field roles on 'Activity'
        db.delete_table('workflow_activity_roles')

        # Deleting model 'Process'
        db.delete_table('workflow_process')

        # Deleting model 'Application'
        db.delete_table('workflow_application')

        # Deleting model 'PushApplication'
        db.delete_table('workflow_pushapplication')

        # Deleting model 'Transition'
        db.delete_table('workflow_transition')

        # Deleting model 'UserProfile'
        db.delete_table('workflow_userprofile')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'workflow.activity': {
            'Meta': {'unique_together': "(('title', 'process'),)", 'object_name': 'Activity'},
            'app_param': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'application': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'activities'", 'null': 'True', 'to': "orm['workflow.Application']"}),
            'autofinish': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'autostart': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'join_mode': ('django.db.models.fields.CharField', [], {'default': "'xor'", 'max_length': '3'}),
            'kind': ('django.db.models.fields.CharField', [], {'default': "'standard'", 'max_length': '10'}),
            'process': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'activities'", 'to': "orm['workflow.Process']"}),
            'push_application': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'push_activities'", 'null': 'True', 'to': "orm['workflow.PushApplication']"}),
            'pushapp_param': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'roles': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'activities'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['auth.Group']"}),
            'split_mode': ('django.db.models.fields.CharField', [], {'default': "'and'", 'max_length': '3'}),
            'subflow': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'parent_activities'", 'null': 'True', 'to': "orm['workflow.Process']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'workflow.application': {
            'Meta': {'object_name': 'Application'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'suffix': ('django.db.models.fields.CharField', [], {'default': "'w'", 'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'workflow.process': {
            'Meta': {'object_name': 'Process'},
            'begin': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'bprocess'", 'null': 'True', 'to': "orm['workflow.Activity']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'end': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'eprocess'", 'null': 'True', 'to': "orm['workflow.Activity']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'priority': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'workflow.pushapplication': {
            'Meta': {'object_name': 'PushApplication'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'workflow.transition': {
            'Meta': {'object_name': 'Transition'},
            'condition': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'input': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'transition_inputs'", 'to': "orm['workflow.Activity']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'output': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'transition_outputs'", 'to': "orm['workflow.Activity']"}),
            'precondition': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'process': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'transitions'", 'to': "orm['workflow.Process']"})
        },
        'workflow.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_notif': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 12, 4, 0, 0)'}),
            'nb_wi_notif': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'notif_delay': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'notified': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'urgent_priority': ('django.db.models.fields.IntegerField', [], {'default': '5'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'}),
            'web_host': ('django.db.models.fields.CharField', [], {'default': "'localhost:8000'", 'max_length': '100'})
        }
    }

    complete_apps = ['workflow']