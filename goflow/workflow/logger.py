import logging
from django.conf import settings
from django.db.models import get_model
import sys

class Log(object):
    def __init__(self, module):
        self.log = logging.getLogger(module)
        # self._event = get_model('runtime', 'Event').objects

    def __getattr__(self, name):
        try:
            return getattr(self.log, name)
        except AttributeError, e:
            return getattr(self, name)

    def __call__(self, *args):
        if len(args) == 0: 
            return
        elif len(args) == 1:
            self.log.info(args[0] )
        else:
            self.log.info(u" ".join([unicode(i) for i in args]))

    def event(self, msg, workitem):
        # self._event.create(name=msg, workitem=workitem)
        self.log.info(u'EVENT: [%s] %s' % (workitem.__unicode__(), msg))
