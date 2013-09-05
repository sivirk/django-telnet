# -*- coding: utf-8 -*-

import datetime

from optparse import make_option

from django.core.management.base import BaseCommand

import gevent
import gevent.server

from telnet.handlers import DjangoCommandHandler


class Command(BaseCommand):

    option_list = BaseCommand.option_list + (
        make_option('--addr',
                    action='store',
                    dest='addr',
                    default='',
                    help='Bind addr'),
        make_option('--port',
                    action='store',
                    dest='port',
                    default=8023,
                    help='Bind port'),)

    help = u'Вывод информации об абоненте'

    def handle(self, *args, **options):
        addr = options.get('addr')
        port = options.get('port')

        print 'Server started', datetime.datetime.now(), '\t on port', port
        try:
            server = gevent.server.StreamServer((addr, port), DjangoCommandHandler.streamserver_handle)
            server.serve_forever()
        except KeyboardInterrupt:
            print 'Stopped', datetime.datetime.now()
