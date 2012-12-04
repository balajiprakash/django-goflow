# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ProcessInstance'
        db.create_table('runtime_processinstance', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('process', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='instances', null=True, to=orm['workflow.Process'])),
            ('creationTime', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='instances', to=orm['auth.User'])),
            ('status', self.gf('django.db.models.fields.CharField')(default='initiated', max_length=10)),
            ('old_status', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('condition', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal('runtime', ['ProcessInstance'])

        # Adding model 'WorkItem'
        db.create_table('runtime_workitem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='workitems', null=True, to=orm['auth.User'])),
            ('instance', self.gf('django.db.models.fields.related.ForeignKey')(related_name='workitems', to=orm['runtime.ProcessInstance'])),
            ('activity', self.gf('django.db.models.fields.related.ForeignKey')(related_name='workitems', to=orm['workflow.Activity'])),
            ('workitem_from', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='workitems_to', null=True, to=orm['runtime.WorkItem'])),
            ('blocked', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('priority', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('status', self.gf('django.db.models.fields.CharField')(default='inactive', max_length=10)),
        ))
        db.send_create_signal('runtime', ['WorkItem'])

        # Adding M2M table for field others_workitems_from on 'WorkItem'
        db.create_table('runtime_workitem_others_workitems_from', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_workitem', models.ForeignKey(orm['runtime.workitem'], null=False)),
            ('to_workitem', models.ForeignKey(orm['runtime.workitem'], null=False))
        ))
        db.create_unique('runtime_workitem_others_workitems_from', ['from_workitem_id', 'to_workitem_id'])

        # Adding M2M table for field push_roles on 'WorkItem'
        db.create_table('runtime_workitem_push_roles', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('workitem', models.ForeignKey(orm['runtime.workitem'], null=False)),
            ('group', models.ForeignKey(orm['auth.group'], null=False))
        ))
        db.create_unique('runtime_workitem_push_roles', ['workitem_id', 'group_id'])

        # Adding M2M table for field pull_roles on 'WorkItem'
        db.create_table('runtime_workitem_pull_roles', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('workitem', models.ForeignKey(orm['runtime.workitem'], null=False)),
            ('group', models.ForeignKey(orm['auth.group'], null=False))
        ))
        db.create_unique('runtime_workitem_pull_roles', ['workitem_id', 'group_id'])

        # Adding model 'Event'
        db.create_table('runtime_event', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('workitem', self.gf('django.db.models.fields.related.ForeignKey')(related_name='events', to=orm['runtime.WorkItem'])),
        ))
        db.send_create_signal('runtime', ['Event'])


    def backwards(self, orm):
        # Deleting model 'ProcessInstance'
        db.delete_table('runtime_processinstance')

        # Deleting model 'WorkItem'
        db.delete_table('runtime_workitem')

        # Removing M2M table for field others_workitems_from on 'WorkItem'
        db.delete_table('runtime_workitem_others_workitems_from')

        # Removing M2M table for field push_roles on 'WorkItem'
        db.delete_table('runtime_workitem_push_roles')

        # Removing M2M table for field pull_roles on 'WorkItem'
        db.delete_table('runtime_workitem_pull_roles')

        # Deleting model 'Event'
        db.delete_table('runtime_event')


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
        'runtime.event': {
            'Meta': {'object_name': 'Event'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'workitem': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'events'", 'to': "orm['runtime.WorkItem']"})
        },
        'runtime.processinstance': {
            'Meta': {'object_name': 'ProcessInstance'},
            'condition': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'creationTime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'old_status': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'process': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'instances'", 'null': 'True', 'to': "orm['workflow.Process']"}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'initiated'", 'max_length': '10'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'instances'", 'to': "orm['auth.User']"})
        },
        'runtime.workitem': {
            'Meta': {'object_name': 'WorkItem'},
            'activity': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'workitems'", 'to': "orm['workflow.Activity']"}),
            'blocked': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instance': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'workitems'", 'to': "orm['runtime.ProcessInstance']"}),
            'others_workitems_from': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'others_workitems_from_rel_+'", 'null': 'True', 'to': "orm['runtime.WorkItem']"}),
            'priority': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'pull_roles': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'pull_workitems'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['auth.Group']"}),
            'push_roles': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'push_workitems'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['auth.Group']"}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'inactive'", 'max_length': '10'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'workitems'", 'null': 'True', 'to': "orm['auth.User']"}),
            'workitem_from': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'workitems_to'", 'null': 'True', 'to': "orm['runtime.WorkItem']"})
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
        }
    }

    complete_apps = ['runtime']